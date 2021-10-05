# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'options_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_options(object):
    def setupUi(self, options):
        options.setObjectName("options")
        options.resize(565, 308)
        self.verticalLayout = QtWidgets.QVBoxLayout(options)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(options)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.spinBoxNbParts = QtWidgets.QSpinBox(options)
        self.spinBoxNbParts.setMinimum(1)
        self.spinBoxNbParts.setMaximum(200)
        self.spinBoxNbParts.setObjectName("spinBoxNbParts")
        self.horizontalLayout.addWidget(self.spinBoxNbParts)
        self.label_4 = QtWidgets.QLabel(options)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.spinBoxStarttIndex = QtWidgets.QSpinBox(options)
        self.spinBoxStarttIndex.setMaximum(1000)
        self.spinBoxStarttIndex.setProperty("value", 1)
        self.spinBoxStarttIndex.setObjectName("spinBoxStarttIndex")
        self.horizontalLayout.addWidget(self.spinBoxStarttIndex)
        self.pushButtonAutoInc = QtWidgets.QPushButton(options)
        self.pushButtonAutoInc.setObjectName("pushButtonAutoInc")
        self.horizontalLayout.addWidget(self.pushButtonAutoInc)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_5 = QtWidgets.QLabel(options)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.spinBoxMaxIndex = QtWidgets.QSpinBox(options)
        self.spinBoxMaxIndex.setMinimum(1)
        self.spinBoxMaxIndex.setMaximum(10000)
        self.spinBoxMaxIndex.setProperty("value", 100)
        self.spinBoxMaxIndex.setObjectName("spinBoxMaxIndex")
        self.horizontalLayout.addWidget(self.spinBoxMaxIndex)
        self.pushButtonAutoRand = QtWidgets.QPushButton(options)
        self.pushButtonAutoRand.setObjectName("pushButtonAutoRand")
        self.horizontalLayout.addWidget(self.pushButtonAutoRand)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(options)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.pushButtonResetOffset = QtWidgets.QPushButton(options)
        self.pushButtonResetOffset.setObjectName("pushButtonResetOffset")
        self.verticalLayout_2.addWidget(self.pushButtonResetOffset)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.tableTemp = QtWidgets.QTableWidget(options)
        self.tableTemp.setObjectName("tableTemp")
        self.tableTemp.setColumnCount(6)
        self.tableTemp.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableTemp.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTemp.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTemp.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTemp.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTemp.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTemp.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTemp.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTemp.setHorizontalHeaderItem(5, item)
        self.horizontalLayout_2.addWidget(self.tableTemp)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(options)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.comboBoxWorkMode = QtWidgets.QComboBox(options)
        self.comboBoxWorkMode.setObjectName("comboBoxWorkMode")
        self.comboBoxWorkMode.addItem("")
        self.comboBoxWorkMode.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBoxWorkMode)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButtonLogFilesFolder = QtWidgets.QPushButton(options)
        self.pushButtonLogFilesFolder.setObjectName("pushButtonLogFilesFolder")
        self.horizontalLayout_5.addWidget(self.pushButtonLogFilesFolder)
        self.lineEditLogFilesFolder = QtWidgets.QLineEdit(options)
        self.lineEditLogFilesFolder.setObjectName("lineEditLogFilesFolder")
        self.horizontalLayout_5.addWidget(self.lineEditLogFilesFolder)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButtonCancel = QtWidgets.QPushButton(options)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout_4.addWidget(self.pushButtonCancel)
        self.pushButtonOk = QtWidgets.QPushButton(options)
        self.pushButtonOk.setObjectName("pushButtonOk")
        self.horizontalLayout_4.addWidget(self.pushButtonOk)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(options)
        QtCore.QMetaObject.connectSlotsByName(options)

    def retranslateUi(self, options):
        _translate = QtCore.QCoreApplication.translate
        options.setWindowTitle(_translate("options", "Settings"))
        self.label_3.setText(_translate("options", "NbParts"))
        self.label_4.setText(_translate("options", "StartIndex"))
        self.pushButtonAutoInc.setText(_translate("options", "Parts Auto Inc "))
        self.label_5.setText(_translate("options", "Max Rand"))
        self.pushButtonAutoRand.setText(_translate("options", "Parts Auto Rand"))
        self.label.setText(_translate("options", "Temperatures Offset"))
        self.pushButtonResetOffset.setText(_translate("options", "ResetOffsetTable"))
        item = self.tableTemp.verticalHeaderItem(0)
        item.setText(_translate("options", "Temp"))
        item = self.tableTemp.verticalHeaderItem(1)
        item.setText(_translate("options", "TempOffset"))
        item = self.tableTemp.horizontalHeaderItem(0)
        item.setText(_translate("options", "Temp1"))
        item = self.tableTemp.horizontalHeaderItem(1)
        item.setText(_translate("options", "Temp2"))
        item = self.tableTemp.horizontalHeaderItem(2)
        item.setText(_translate("options", "Temp3"))
        item = self.tableTemp.horizontalHeaderItem(3)
        item.setText(_translate("options", "Temp4"))
        item = self.tableTemp.horizontalHeaderItem(4)
        item.setText(_translate("options", "Temp5"))
        item = self.tableTemp.horizontalHeaderItem(5)
        item.setText(_translate("options", "Temp6"))
        self.label_2.setText(_translate("options", "Work Mode"))
        self.comboBoxWorkMode.setItemText(0, _translate("options", "Cycle temperatures for each part"))
        self.comboBoxWorkMode.setItemText(1, _translate("options", "Cycle parts for each temperature"))
        self.pushButtonLogFilesFolder.setText(_translate("options", "LogFilesFolder"))
        self.pushButtonCancel.setText(_translate("options", "Cancel"))
        self.pushButtonOk.setText(_translate("options", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    options = QtWidgets.QDialog()
    ui = Ui_options()
    ui.setupUi(options)
    options.show()
    sys.exit(app.exec_())