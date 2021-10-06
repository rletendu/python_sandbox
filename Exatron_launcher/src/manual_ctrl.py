from PyQt5.QtCore import pyqtSignal, QMimeData, QTimer, Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog, QMessageBox, QShortcut
from PyQt5 import QtWidgets
from manual_ctrl_ui import Ui_Dialog as ManualCtrl


class ManualCtrlDialog(QDialog):

    def __init__(self, exatron, parent=None):
        QDialog.__init__(self, parent=parent)
        self.parent = parent
        self.popup = ManualCtrl()
        self.popup.setupUi(self)
        self.exatron = exatron
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timerTick)

    @pyqtSlot()
    def timerTick(self):
        self.popup.labelState.setText(self.exatron.get_state().name)
        pass

    @pyqtSlot()
    def on_pushButtonOk_clicked(self):
        self.timer.stop()
        self.close()
        pass

    @pyqtSlot()
    def on_pushButtonEol_clicked(self):
        self.exatron.end_of_lot()
        pass

    @pyqtSlot()
    def on_pushButtonResult_clicked(self):
        self.exatron.unload_part(self.popup.spinBoxBin.value())
        pass

    @pyqtSlot()
    def on_pushButtonNextPart_clicked(self):
        self.exatron.load_next_part()
        pass

    @pyqtSlot()
    def on_pushButtonSetTemp_clicked(self):
        temp = self.popup.doubleSpinBoxTemp.value()
        shiller = self.popup.comboBox.currentText()
        accuracy = self.popup.doubleSpinBoxAccuracy.value()
        self.exatron.set_temperature(temp, shiller, accuracy)
        pass


    @pyqtSlot()
    def on_pushButtonGetTemp_clicked(self):
        t = self.exatron.get_temperature()
        self.popup.lcdNumber.display(t)
        pass


    @pyqtSlot()
    def on_pushButtonEol_clicked(self):
        self.exatron.end_of_lot()
        pass
