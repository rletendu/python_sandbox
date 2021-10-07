from PyQt5.QtCore import pyqtSignal, QMimeData, QTimer, Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog, QMessageBox, QShortcut
from PyQt5 import QtWidgets
from exatron import ExatronState
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
        if self.exatron is None:
            self.prevExatronState = ExatronState.OFFLINE
        else:
            self.prevExatronState = self.exatron.get_state()

    @pyqtSlot()
    def timerTick(self):
        if self.exatron is None:
            return
        new_state = self.exatron.get_state()
        self.popup.labelState.setText(new_state.name)
        if new_state != self.prevExatronState:
            if new_state == ExatronState.READY:
                self.buttonsSetEnable(True)
            else:
                self.buttonsSetEnable(False)
        self.prevExatronState = new_state

    def buttonsSetEnable(self, state):
        self.popup.pushButtonEol.setEnabled(state)
        self.popup.pushButtonGetTemp.setEnabled(state)
        self.popup.pushButtonNextPart.setEnabled(state)
        self.popup.pushButtonSetTemp.setEnabled(state)
        self.popup.pushButtonResult.setEnabled(state)

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
