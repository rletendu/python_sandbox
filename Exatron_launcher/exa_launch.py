import logging
import argparse
from PyQt5.QtCore import pyqtSignal, QMimeData, QTimer, Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog, QMessageBox, QShortcut
from PyQt5.QtGui import QTextCursor, QKeySequence
from PyQt5 import QtWidgets
from time import sleep
from queue import Queue
from exa import Exa
from exa_launch_ui import Ui_ExaJobLauncher
import serial
import serial.tools.list_ports
import socket
import traceback
from exa_job_thread import ExaJobSignals,ExaJobThread
import configparser
import os


LOGGING_FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(lineno)d :: %(funcName)s :: %(message)s'
GUI_CONFIG_FILE = "exa_launch.ini"

def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error catched!:")
    print("error message:\n", tb)
    QtWidgets.QApplication.quit()
    # or QtWidgets.QApplication.exit(0)


class StdStreamThreadSignals(QObject):
    abort_signal = pyqtSignal()
    go_signal = pyqtSignal()


class WriteStream(object):
    """
        The new Stream Object which replaces the default stream associated with sys.stdout
        This object just puts data in a queue!
         -->> Finally used for print redirection in GUI text area and log_file
        """
    count = 0

    def __init__(self, queue):
        self.__class__.count += 1
        self.queue = queue

    def write(self, text):
        self.queue.put(text)

    def flush(self):
        pass

    def __del__(self):
        self.__class__.count -= 1
        if self.__class__.count == 0:
            pass


class StdStreamThread(QObject):
    """
        A QObject (to be run in a QThread) which sits waiting for data to come through a Queue.Queue().
        It blocks until data is available, and one it has got something from the queue, it sends
        it to the "MainThread" by emitting a Qt Signal
        -->> Finally used for print redirection in GUI text area
        """
    write_signal = pyqtSignal(str)

    def __init__(self, queue, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.queue = queue
        self.run_flag = True

    @pyqtSlot()
    def run(self):
        count = 0
        while self.run_flag:
            text = self.queue.get()
            self.write_signal.emit(text)

    @pyqtSlot()
    def abort(self):
        self.run_flag = False


class MainWindow(QMainWindow, Ui_ExaJobLauncher):

    changed = pyqtSignal(QMimeData)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.load_ini_file()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.exatron = None
        self.connectButton.clicked.connect(self.connect)
        self.startButton.clicked.connect(self.start)
        self.abortButton.clicked.connect(self.abort)
        self.actionopen.triggered.connect(self.menuOpen)
        self.actionsave.triggered.connect(self.menuSave)
        self.actionSave_As.triggered.connect(self.menuSaveAs)
        self.actiondebug.setCheckable(True)
        self.actiondebug.triggered.connect(self.debug_enable)
        self.saveSc = QShortcut(QKeySequence('Ctrl+S'), self)
        self.saveSc.activated.connect(self.menuSave)
        self.openSc = QShortcut(QKeySequence('Ctrl+O'), self)
        self.openSc.activated.connect(self.menuOpen)

        self.sig_job = None
        self.worker = None
        self.filename = None

        local_ip = socket.gethostbyname(socket.gethostname())
        self.interfaceBox.addItem(local_ip)
        com_list = serial.tools.list_ports.comports()
        for com in com_list:
            self.interfaceBox.addItem(com.device)
            break
        self.interfaceBox.addItem("demo")
        self.abortButton.setEnabled(False)
        self.startButton.setEnabled(False)
        self.statusbar.showMessage('Select an Exatron Interface')

    def load_ini_file(self):
        config = configparser.ConfigParser()
        f = open(GUI_CONFIG_FILE, "a+")
        if os.stat(GUI_CONFIG_FILE).st_size == 0:
            # ini file does not exits, creating
            f.close()
            config['LAST_SETTINGS'] = {'suite_file': '', 'com_port': ''}
            with open(GUI_CONFIG_FILE, "w") as gui_config_file:
                config.write(gui_config_file)

    def write_ini_fiel(self):
        pass

    @pyqtSlot()
    def debug_enable(self):
        if self.actiondebug.isChecked():
            print("DEBUG mode ON")
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            print("DEBUG mode OFF")
            logging.getLogger().setLevel(logging.ERROR)

    @pyqtSlot()
    def menuOpen(self):
        options = configparser.ConfigParser()
        self.filename, s = QFileDialog.getOpenFileName(self, "Select Exajob file...")
        options.read(self.filename)
        self.partsEdit.setText( options["EXAJOB"]["parts"])
        self.tempEdit.setText( options["EXAJOB"]["temperatures"])
        self.cmdLineEdit.setText( options["EXAJOB"]["cmdline"])
        self.tcpPortBox.setValue(int(options["EXAJOB"]["exatron_tcp_port"]))
        self.interfaceBox.setCurrentText(options["EXAJOB"]["exatron_interface"])
        self.tempSoakSpinBox.setValue(int(options["EXAJOB"]["temp_soak_time"]))
        self.tempAccuracySpinBox.setValue(float(options["EXAJOB"]["temp_accuracy"]))
        self.setWindowTitle(self.filename)

    @pyqtSlot()
    def menuSave(self):
        if self.filename is not None:
            self.save(self.filename)
        else:
            self.menuSaveAs()

    @pyqtSlot()
    def menuSaveAs(self):
        self.filename, filter = QFileDialog.getSaveFileName(self, 'Save File')
        self.save(self.filename)

    def save(self, f):
        options = configparser.ConfigParser()
        options["EXAJOB"] = {'cmdline':self.cmdLineEdit.text(), 'parts':self.partsEdit.text(), 'temperatures':self.tempEdit.text(),
        'exatron_interface' : self.interfaceBox.currentText(), 'exatron_tcp_port':self.tcpPortBox.value(),
                             'temp_soak_time' : self.tempSoakSpinBox.value(), 'temp_accuracy': self.tempAccuracySpinBox.value()}
        with open(f,'w') as optionsFile:
            options.write(optionsFile)
        self.setWindowTitle(self.filename)

    def closeEvent(self, event):
        result = QMessageBox.question(self, "Confirm Exit...", "Are you sure you want to exit ?", QMessageBox.Yes | QMessageBox.No)
        event.ignore()
        if result == QMessageBox.Yes:
            event.accept()
            config = configparser.ConfigParser()
            config['LAST_SETTINGS'] = {}
            config['LAST_SETTINGS']['suite_file'] = self.param_file
            config['LAST_SETTINGS']['com_port'] = self.comboBox_com_list.currentText()
            with open(GUI_CONFIG_FILE, 'w') as configfile:
                config.write(configfile)
        event.accept()

    @pyqtSlot()
    def connect(self):
        if self.exatron is None:
            interface = self.interfaceBox.currentText()
            if interface.startswith("COM"):
                self.exatron = Exa(com_port=interface)
                self.statusbar.showMessage('{} Openned'.format(interface))
            elif interface == "demo":
                self.exatron = Exa(com_port=interface, demo=True)
                self.statusbar.showMessage('Using Demo Handler')
            else:
                self.exatron = Exa(tcp_port=self.tcpPortBox.value())
                self.statusbar.showMessage('Server {} waiting client connection'.format(interface))
            self.timer.start(500)
            self.sig_job = ExaJobSignals()
            self.accuracy = self.tempAccuracySpinBox.value()
            self.soak_time = self.tempSoakSpinBox.value()
            self.worker = ExaJobThread(self.exatron, self.sig_job, temp_soak=self.soak_time, temp_accuracy=self.accuracy)
            self.sig_job.start_suite.connect(self.worker.run)
            self.sig_job.notify_progress.connect(self.notify_progress)
            self.sig_job.all_done.connect(self.all_done)
            self.suite_thread = QThread()
            self.worker.moveToThread(self.suite_thread)
            self.suite_thread.start()


    @pyqtSlot()
    def start(self):
        self.abortButton.setEnabled(True)
        self.startButton.setEnabled(False)

        self.part_list = self.partsEdit.text().replace(" ","").split(",")
        for i in range(len(self.part_list)):
            self.part_list[i] = int(self.part_list[i])
        self.temp_list = self.tempEdit.text().replace(" ","").split(",")
        for i in range(len(self.temp_list)):
            self.temp_list[i] = int(self.temp_list[i])
        self.cmd = self.cmdLineEdit.text()

        print('Starting Exatron job with parts : {} over temperature {}'.format(self.part_list, self.temp_list))


        self.sig_job.start_suite.emit(self.temp_list, self.part_list, self.cmd)

    @pyqtSlot(str, int, int)
    def notify_progress(self, text, part, temp):
        self.cur_part.setText("Curent Part: {}".format(part))
        self.cur_temp.setText("Curent Temp: {}".format(temp))
        self.tempProgressBar.setValue(100*((self.temp_list.index(temp)+1)/len(self.temp_list)))
        self.partProgressBar.setValue(100*((self.part_list.index(part)+1)/len(self.part_list)))
        if len(text):
            self.statusbar.showMessage(text)

    @pyqtSlot()
    def Time(self):
        if self.exatron.is_connected():
            self.statusbar.showMessage("Handler client is connected, waiting ready")
        if self.exatron.is_ready():
            self.timer.stop()
            self.statusbar.showMessage("Handler is ready!")
            self.abortButton.setEnabled(False)
            self.startButton.setEnabled(True)
        pass

    @pyqtSlot()
    def abort(self):
        if self.worker is not None:
            self.worker.abort()

    @pyqtSlot()
    def all_done(self):
        self.abortButton.setEnabled(False)
        self.startButton.setEnabled(True)

    @pyqtSlot(str)
    def append_log(self, text):
        self.logBrowser.moveCursor(QTextCursor.End)
        self.logBrowser.insertPlainText(text)


if __name__ == '__main__':
    import sys
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    if 'pydevd' not in sys.modules:
        stream_redirection = True
        print("Running out of Debug, stream redirection Enable")
    else:
        stream_redirection = False
        print("Running in Debug, no stream redirection")

    if stream_redirection:
        # Create Queue and redirect sys.stdout to this queue
        queue = Queue()
        saved_stdout = sys.stdout
        saved_stderr = sys.stderr
        sys.stdout = WriteStream(queue)
        sys.stderr = WriteStream(queue)

    logging.basicConfig(level=logging.ERROR, format=LOGGING_FORMAT,)
    log = logging.getLogger(__name__)
    log.setLevel(logging.ERROR)

    # Create thread that will listen on the other end of the queue, and send the text to the textedit in our application
    # Detects the application is running within debug session, in that case do not redirect stdout to gui
    if stream_redirection:
        sig = StdStreamThreadSignals()
        stream_thread = QThread()
        # thread.setPriority(QThread.HighPriority)
        stream_worker = StdStreamThread(queue)
        sig.abort_signal.connect(stream_worker.abort)
        sig.go_signal.connect(stream_worker.run)
        stream_worker.write_signal.connect(
            window.append_log)
        stream_worker.moveToThread(stream_thread)
        stream_thread.start()
        sig.go_signal.emit()
        sleep(0.5)


    sys.exit(app.exec_())
