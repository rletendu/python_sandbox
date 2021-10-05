from PyQt5.QtCore import pyqtSignal, QMimeData, QTimer, Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog, QMessageBox, QShortcut
from PyQt5.QtGui import QTextCursor, QKeySequence
from PyQt5 import QtWidgets
from options_ui import Ui_options as Options
import random

class OptionsDialog(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.parent = parent
        self.popup = Options()
        self.popup.setupUi(self)
        self.popup.comboBoxWorkMode.setEnabled(False)

    @pyqtSlot()
    def on_pushButtonCancel_clicked(self):
        self.close()
        pass

    @pyqtSlot()
    def on_pushButtonAutoInc_clicked(self):
        nb = self.popup.spinBoxNbParts.value()
        st = self.popup.spinBoxStarttIndex.value()
        s = str(list(range(st,st+nb)))
        self.parent.partsEdit.setText(s.replace('[','').replace(']',''))


    @pyqtSlot()
    def on_pushButtonAutoRand_clicked(self):
        st = self.popup.spinBoxStarttIndex.value()
        nb = self.popup.spinBoxNbParts.value()
        max = self.popup.spinBoxMaxIndex.value()
        v = []
        while len(v)<nb:
            n =random.randint(st, max)
            if n in v:
                continue
            else:
                v.append(n)
        self.parent.partsEdit.setText(str(v).replace('[','').replace(']',''))

    def fillOffsetTable(self, temp_offset):
        nb_temp = len(temp_offset)
        self.popup.tableTemp.setRowCount(2)
        self.popup.tableTemp.setColumnCount(nb_temp)

        for col in range(nb_temp):
            v = QtWidgets.QTableWidgetItem(str(temp_offset[col][0]))
            self.popup.tableTemp.setItem(0,col, QtWidgets.QTableWidgetItem(v))
            v = QtWidgets.QTableWidgetItem(str(temp_offset[col][1]))
            self.popup.tableTemp.setItem(1,col, v)
        self.popup.tableTemp.resizeRowsToContents()
        self.popup.tableTemp.resizeColumnsToContents()

    def readOffsetTable(self):
        l = []
        nb_temp = self.popup.tableTemp.columnCount()
        for col in range(nb_temp):
            t =int(self.popup.tableTemp.item(0,col).text())
            t_offset = int(self.popup.tableTemp.item(1,col).text())
            l.append((t,t_offset))
        return l

    @pyqtSlot()
    def on_pushButtonResetOffset_clicked(self):
        l = [-40,0,25,85,105,125]
        nb_temp = len(l)
        for col in range(nb_temp):
            v = QtWidgets.QTableWidgetItem(str(l[col]))
            self.popup.tableTemp.setItem(0,col, QtWidgets.QTableWidgetItem(v))
            v = QtWidgets.QTableWidgetItem(str(l[col]))
            self.popup.tableTemp.setItem(1,col, v)

    @pyqtSlot()
    def on_pushButtonLogFilesFolder_clicked(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.popup.lineEditLogFilesFolder.setText(file)



