from PyQt5.QtCore import pyqtSignal, QMimeData, QTimer, Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog, QMessageBox, QShortcut
from PyQt5.QtGui import QTextCursor, QKeySequence
from PyQt5 import QtWidgets
from progress_ui import Ui_Dialog as Progress


class Progress_Window(QDialog):
    cancel = pyqtSignal()
    def __init__(self, msg, parent=None):
        QDialog.__init__(self, parent=parent)
        self.popup = Progress()
        self.popup.setupUi(self)
        self.popup.label.setText(msg)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.v = 0
        self.timer.start(10)

    def setMessage(self,msg):
        self.popup.label.setText(msg)
        self.timer.start(10)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.timer.stop()
        self.close()
        self.cancel.emit()

    def loading(self):
        self.v += 1
        if self.v > 100:
            self.v = 0
        self.popup.progressBar.setValue(self.v)