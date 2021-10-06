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
from exatron import ExaTron, ExatronState
from exa_launch_ui import Ui_ExaJobLauncher
import serial
import serial.tools.list_ports
import socket
import traceback
from exa_job_thread import ExaJobSignals,ExaJobThread
import configparser
import os
from progress import Progress_Window
from options import OptionsDialog
from manual_ctrl import ManualCtrlDialog
from enum import Enum
from datetime import datetime
import revision

LOGGING_FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(lineno)d :: %(funcName)s :: %(message)s'
GUI_CONFIG_FILE = "exa_launch.ini"

def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error catched!:")
    print("error message:\n", tb)
    QtWidgets.QApplication.quit()

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
        self.f = open('log.txt',"a")

    def write(self, text):
        self.queue.put(text)
        self.f.write(text)

    def flush(self):
        pass

    def __del__(self):
        self.__class__.count -= 1
        if self.__class__.count == 0:
            self.f.close()


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

    def __del__(self):
        self.f.close()


class testerState(Enum):
        IDLE = 1
        HANDLER_CONNECT_INIT = 2
        WAIT_HANDLER_CONNECT = 3
        WAIT_NEW_JOB_START = 4
        WAIT_HANDLER_READY = 5
        WORKING = 6

class MainWindow(QMainWindow, Ui_ExaJobLauncher):
    changed = pyqtSignal(QMimeData)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('ExaJobLauncher V{}.{} built {}'.format(revision.REVISION, revision.BUILD, revision.BUILD_DATE))
        self.tempOffset =[]
        for t in [-40,0,25,85,105,125]:
            self.tempOffset.append((t,t))
        self.logFolder = os.getcwd()
        self.options = configparser.ConfigParser()
        self.load_ini_file()
        self.recentfiles_menu = self.menuFile.addMenu("&Open Recent")
        self.recentfiles_menu.triggered.connect(self.handle_triggered_recentfile)
        self.last_file = None
        if self.options.has_option('EXAJOB','last_file'):
            self.last_file = self.options['EXAJOB']['last_file']
            self.add_recent_filename(self.last_file)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.testerTick)
        self.exatron = None
        self.connectButton.clicked.connect(self.connect)
        self.startButton.clicked.connect(self.startJob)
        self.abortButton.clicked.connect(self.abortJob)
        self.actionopen.triggered.connect(self.menuOpen)
        self.actionsave.triggered.connect(self.menuSave)
        self.actionsettings.triggered.connect(self.menuSettings)
        self.actionmanual_ctrl.triggered.connect(self.menuManualCtrl)
        self.actionSave_As.triggered.connect(self.menuSaveAs)
        self.actiondebug.setCheckable(True)
        self.actiondebug.triggered.connect(self.debug_enable)
        self.saveSc = QShortcut(QKeySequence('Ctrl+S'), self)
        self.saveSc.activated.connect(self.menuSave)
        self.openSc = QShortcut(QKeySequence('Ctrl+O'), self)
        self.openSc.activated.connect(self.menuOpen)
        self.settingsPanel = OptionsDialog(self)
        self.settingsPanel.popup.pushButtonOk.clicked.connect(self.setttingsOk)
        self.manualCtrlPanel = ManualCtrlDialog(self.exatron, self)
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

        self.progressPanel = Progress_Window(msg="Waiting Handler Connection", parent=self.window())
        self.progressPanel.cancel.connect(self.progressCancelled)
        self.state = testerState.IDLE
        self.flagNewJob = False
        self.logFile = None

    @pyqtSlot(QtWidgets.QAction)
    def handle_triggered_recentfile(self, action):
        f = action.text()
        if os.stat(f).st_size != 0:
            self.filename = f
            self.options.read(self.filename)
            self.options2gui()
            self.setWindowTitle(self.filename)
            print("Loaded {}".format(f))
        else:
            print("{} does not exist".format(f))

    def add_recent_filename(self, filename):
        action = QtWidgets.QAction(filename, self)
        actions = self.recentfiles_menu.actions()
        before_action = actions[0] if actions else None
        self.recentfiles_menu.insertAction(before_action, action)

    def load_ini_file(self):
        f = open(GUI_CONFIG_FILE, "a+")
        if os.stat(GUI_CONFIG_FILE).st_size == 0:
            # ini file does not exits, creating
            f.close()
            self.gui2options()
            #config['LAST_SETTINGS'] = {'suite_file': '', 'com_port': ''}
            with open(GUI_CONFIG_FILE, "w") as gui_config_file:
                self.options.write(gui_config_file)
        else:
            self.options.read(GUI_CONFIG_FILE)
            self.options2gui()

    def write_ini_file(self):
        self.gui2options()
        if self.filename:
            self.options['EXAJOB']['last_file'] =self.filename
        elif self.last_file:
            self.options['EXAJOB']['last_file'] = self.last_file
        with open(GUI_CONFIG_FILE, "w") as gui_config_file:
            self.options.write(gui_config_file)

    @pyqtSlot()
    def debug_enable(self):
        if self.actiondebug.isChecked():
            print("DEBUG mode ON")
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            print("DEBUG mode OFF")
            logging.getLogger().setLevel(logging.ERROR)

    @pyqtSlot()
    def menuSettings(self):
        self.settingsPanel.fillOffsetTable(self.tempOffset)
        if self.logFolder:
            self.settingsPanel.popup.lineEditLogFilesFolder.setText(self.logFolder)
        self.settingsPanel.show()

    @pyqtSlot()
    def menuManualCtrl(self):
        self.manualCtrlPanel.exatron = self.exatron
        self.manualCtrlPanel.timer.start(500)
        self.manualCtrlPanel.show()

    @pyqtSlot()
    def menuOpen(self):
        self.filename, s = QFileDialog.getOpenFileName(self, "Select Exajob file...")
        self.options.read(self.filename)
        self.options2gui()
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
        self.gui2options()
        with open(f,'w') as optionsFile:
            self.options.write(optionsFile)
        self.setWindowTitle(self.filename)

    def gui2options(self):
        self.options["EXAJOB"] = {
            'cmdline':self.cmdLineEdit.text(),
            'parts':self.partsEdit.text(),
            'temperatures':self.tempEdit.text(),
            'exatron_interface' : self.interfaceBox.currentText(),
            'exatron_tcp_port':self.tcpPortBox.value(),
            'temp_soak_time' : self.tempSoakSpinBox.value(), 'temp_accuracy': self.tempAccuracySpinBox.value(),
            'offset_list' : str(self.tempOffset),
            'log_file_folder': str(self.logFolder),
        }

    def options2gui(self):
        self.partsEdit.setText( self.options["EXAJOB"]["parts"])
        self.tempEdit.setText( self.options["EXAJOB"]["temperatures"])
        self.cmdLineEdit.setText( self.options["EXAJOB"]["cmdline"])
        self.tcpPortBox.setValue(int(self.options["EXAJOB"]["exatron_tcp_port"]))
        self.interfaceBox.setCurrentText(self.options["EXAJOB"]["exatron_interface"])
        self.tempSoakSpinBox.setValue(int(self.options["EXAJOB"]["temp_soak_time"]))
        self.tempAccuracySpinBox.setValue(float(self.options["EXAJOB"]["temp_accuracy"]))
        self.tempOffset = eval(self.options["EXAJOB"]["offset_list"])
        self.logFolder = self.options["EXAJOB"]['log_file_folder']

    def closeEvent(self, event):
        result = QMessageBox.question(self, "Confirm Exit...", "Are you sure you want to exit ?", QMessageBox.Yes | QMessageBox.No)
        event.ignore()
        if result == QMessageBox.Yes:
            event.accept()
            self.write_ini_file()
        if self.exatron:
            self.exatron.close()
        if self.logFile:
            self.logFile.close()
        event.accept()

    @pyqtSlot()
    def connect(self):
        if self.exatron is None:
            interface = self.interfaceBox.currentText()
            if interface.startswith("COM"):
                self.exatron = ExaTron(com_port=interface)
                self.statusbar.showMessage('{} Openned'.format(interface))
            elif interface == "demo":
                self.exatron = ExaTron(com_port=interface, demo=True)
                self.statusbar.showMessage('Using Demo Handler')
            else:
                self.exatron = ExaTron(tcp_port=self.tcpPortBox.value())
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
            self.state = testerState.HANDLER_CONNECT_INIT


    @pyqtSlot()
    def progressCancelled(self):
        print("Cancelled!!")

    @pyqtSlot()
    def setttingsOk(self):
        self.tempOffset = self.settingsPanel.readOffsetTable()
        self.logFolder = self.settingsPanel.popup.lineEditLogFilesFolder.text()
        self.settingsPanel.close()

    @pyqtSlot()
    def startJob(self):
        self.abortButton.setEnabled(True)
        self.startButton.setEnabled(False)
        self.part_list = self.partsEdit.text().replace(" ","").split(",")
        for i in range(len(self.part_list)):
            self.part_list[i] = int(self.part_list[i])
        self.temp_list = self.tempEdit.text().replace(" ","").split(",")
        for i in range(len(self.temp_list)):
            self.temp_list[i] = int(self.temp_list[i])
        self.cmd = self.cmdLineEdit.text()
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d_%H%M%S")
        filename = "exa_launch_{}.log".format(dt_string)
        f = os.path.join(self.logFolder, filename)
        if self.logFile:
            self.logFile.close()
        self.logFile =open(f, "a")
        self.flagNewJob = True

    @pyqtSlot(str, int, int)
    def notify_progress(self, text, part, temp):
        self.cur_part.setText("Curent Part: {}".format(part))
        self.cur_temp.setText("Curent Temp: {}".format(temp))
        self.tempProgressBar.setValue(int(100*((self.temp_list.index(temp)+1)/len(self.temp_list))))
        self.partProgressBar.setValue(int(100*((self.part_list.index(part)+1)/len(self.part_list))))
        if len(text):
            self.statusbar.showMessage(text)

    @pyqtSlot()
    def testerTick(self):
        self.handlerState.setText(self.exatron.get_state().name)
        if self.state == testerState.IDLE:
            pass
        elif self.state == testerState.HANDLER_CONNECT_INIT:
            self.progressPanel.setMessage("Waiting Handler connection, operator should start Exatron Application")
            self.progressPanel.show()
            self.state = testerState.WAIT_HANDLER_CONNECT
        elif self.state == testerState.WAIT_HANDLER_CONNECT:
            if self.exatron.get_state() == ExatronState.CONNECTED:
                self.progressPanel.close()
                self.state = testerState.WAIT_NEW_JOB_START
                self.abortButton.setEnabled(False)
                self.startButton.setEnabled(True)
                self.statusbar.showMessage('Handler connected, start a job')
        elif self.state == testerState.WAIT_NEW_JOB_START:
            if self.flagNewJob:
                self.progressPanel.setMessage("Waiting Ready from handler, operator should start AUTO mode job")
                self.progressPanel.show()
                self.flagNewJob = False
                self.state = testerState.WAIT_HANDLER_READY
        elif self.state == testerState.WAIT_HANDLER_READY:
            if self.exatron.get_state() == ExatronState.READY:
                self.progressPanel.close()
                print('Starting Exatron job with parts : {} over temperature {}'.format(self.part_list, self.temp_list))
                self.sig_job.start_suite.emit(self.temp_list, self.part_list, self.cmd, self.tempOffset)
                self.state = testerState.WORKING
                self.abortButton.setEnabled(True)
                self.startButton.setEnabled(False)
        elif self.state == testerState.WORKING:
            pass

    @pyqtSlot()
    def abortJob(self):
        if self.worker is not None:
            self.worker.abort()
        if self.logFile:
            self.logFile.close()

    @pyqtSlot()
    def all_done(self):
        self.abortButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.state = testerState.WAIT_NEW_JOB_START
        if self.logFile:
            pass
            self.logFile.flush()

    @pyqtSlot(str)
    def append_log(self, text):
        self.logBrowser.moveCursor(QTextCursor.End)
        self.logBrowser.insertPlainText(text)
        if self.logFile:
            pass
            self.logFile.write(text)


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
