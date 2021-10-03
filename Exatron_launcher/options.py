from PyQt5.QtCore import pyqtSignal, QMimeData, QTimer, Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog, QMessageBox, QShortcut
from PyQt5.QtGui import QTextCursor, QKeySequence
from PyQt5 import QtWidgets
from options_ui import Ui_options as Options


class OptionsDialog(QDialog):

    def __init__(self, msg, parent=None):
        QDialog.__init__(self, parent=parent)
        self.parent = parent
        self.popup = Options()
        self.popup.setupUi(self)
        self.popup.label.setText(msg)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)


    @pyqtSlot()
    def on_pushButton_clicked(self):
        pass


    def loading(self):
        self.v += 1
        if self.v > 100:
            self.v = 0
        self.popup.progressBar.setValue(self.v)