
#from PyQt5.QtCore import (QAbstractItemModel, QFile, QIODevice, QItemSelectionModel, QModelIndex, Qt)
from PyQt5.QtCore import pyqtSignal, QMimeData, QTimer, Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from time import sleep
from queue import Queue

from ui import Ui_MainWindow


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
        #loadUi('ui.ui', self)
        self.setupUi(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.timer.start(100)

    def on_pushButton_clicked(self):
        self.label.setText("toto")

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasUrls():
            filename = "".join([url.path() for url in mimeData.urls()])
            filename = filename[1:]
            self.label.setText(filename)
            file = open(filename, "r")
            self.textBrowser.setText(file.read())
            file.close()
        event.acceptProposedAction()

    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        self.changed.emit(event.mimeData())

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def Time(self):
        i = self.lcdNumber_2.value() + 1
        self.lcdNumber_2.display(i)
        print("Hello {}".format(i))

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

    sys.exit(app.exec_())
