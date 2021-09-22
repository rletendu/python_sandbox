import logging
import argparse
from PyQt5.QtCore import pyqtSignal, QMimeData, QTimer, Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtWidgets
from time import sleep
from queue import Queue
from exa import Exa
from exa_ui import Ui_MainWindow
import serial
import serial.tools.list_ports
import socket



LOGGING_FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(lineno)d :: %(funcName)s :: %(message)s'

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


class MainWindow(QMainWindow, Ui_MainWindow):

    changed = pyqtSignal(QMimeData)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.timer.start(100)
        self.setTempButton.clicked.connect(self.settemp)
        self.exatron = None
        self.connectButton.clicked.connect(self.connect)
        self.pichPartButton.clicked.connect(self.pickNextPart)
        self.eolButton.clicked.connect(self.endOfLot)
        self.unLoadpart.clicked.connect(self.unloadPart)
        self.getTempButton.clicked.connect(self.gettemp)
        local_ip = socket.gethostbyname(socket.gethostname())
        self.interfaceBox.addItem(local_ip)
        com_list = serial.tools.list_ports.comports()
        for com in com_list:
            self.interfaceBox.addItem(com.device)
            break

    def closeEvent(self, event):
        self.exatron.__del__()
        event.accept()

    @pyqtSlot()
    def connect(self):
        if self.exatron is None:
            interface = self.interfaceBox.currentText()
            if interface.startswith("COM"):
                self.exatron = Exa(com_port=interface)
            else:
                self.exatron = Exa(tcp_port=self.tcpPortBox.value())
            
    @pyqtSlot()
    def settemp(self):
        t = self.setTempVal.value()
        s = self.tempRangeBox.currentText()
        self.exatron.set_temperature(t)
        print('Settemp {} {}'.format(t,s))
        pass

    @pyqtSlot()
    def gettemp(self):
        t = self.exatron.get_temperature()
        self.getTempVal.value(t)

    @pyqtSlot()
    def endOfLot(self):
        self.exatron.end_of_lot()

    @pyqtSlot()
    def pickNextPart(self):
        self.exatron.load_next_part()

    @pyqtSlot()
    def unloadPart(self):
        self.exatron.unload_part(self.binBox.value())

    @pyqtSlot()
    def Time(self):
        pass

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

    queue = Queue()
    saved_stdout = sys.stdout
    saved_stderr = sys.stderr
    sys.stdout = WriteStream(queue)
    sys.stderr = WriteStream(queue)

    logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT,)
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    # Create thread that will listen on the other end of the queue, and send the text to the textedit in our application
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

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("Done")
