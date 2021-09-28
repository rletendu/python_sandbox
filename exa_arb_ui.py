# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'exa_arb_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ExatronARB(object):
    def setupUi(self, ExatronARB):
        ExatronARB.setObjectName("ExatronARB")
        ExatronARB.resize(811, 555)
        ExatronARB.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(ExatronARB)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.interfaceBox = QtWidgets.QComboBox(self.centralwidget)
        self.interfaceBox.setObjectName("interfaceBox")
        self.horizontalLayout_3.addWidget(self.interfaceBox)
        self.tcpPortBox = QtWidgets.QSpinBox(self.centralwidget)
        self.tcpPortBox.setMaximum(65535)
        self.tcpPortBox.setProperty("value", 4000)
        self.tcpPortBox.setObjectName("tcpPortBox")
        self.horizontalLayout_3.addWidget(self.tcpPortBox)
        self.connectButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectButton.setObjectName("connectButton")
        self.horizontalLayout_3.addWidget(self.connectButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.aboartButton = QtWidgets.QPushButton(self.centralwidget)
        self.aboartButton.setObjectName("aboartButton")
        self.horizontalLayout_3.addWidget(self.aboartButton)
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setObjectName("startButton")
        self.horizontalLayout_3.addWidget(self.startButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout.addWidget(self.line_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.cmdLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.cmdLineEdit.setObjectName("cmdLineEdit")
        self.horizontalLayout_4.addWidget(self.cmdLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.tempEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.tempEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.tempEdit.setMaxLength(50)
        self.tempEdit.setObjectName("tempEdit")
        self.horizontalLayout.addWidget(self.tempEdit)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.tempSoakSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.tempSoakSpinBox.setMinimum(1)
        self.tempSoakSpinBox.setSingleStep(10)
        self.tempSoakSpinBox.setObjectName("tempSoakSpinBox")
        self.horizontalLayout.addWidget(self.tempSoakSpinBox)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.tempAccuracySpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.tempAccuracySpinBox.setDecimals(1)
        self.tempAccuracySpinBox.setMinimum(0.0)
        self.tempAccuracySpinBox.setMaximum(10.0)
        self.tempAccuracySpinBox.setSingleStep(0.1)
        self.tempAccuracySpinBox.setProperty("value", 2.0)
        self.tempAccuracySpinBox.setObjectName("tempAccuracySpinBox")
        self.horizontalLayout.addWidget(self.tempAccuracySpinBox)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout.addWidget(self.line_4)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cur_temp = QtWidgets.QLabel(self.centralwidget)
        self.cur_temp.setObjectName("cur_temp")
        self.horizontalLayout.addWidget(self.cur_temp)
        self.tempProgressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.tempProgressBar.setProperty("value", 0)
        self.tempProgressBar.setObjectName("tempProgressBar")
        self.horizontalLayout.addWidget(self.tempProgressBar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout.addWidget(self.line_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.partsEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.partsEdit.setObjectName("partsEdit")
        self.horizontalLayout_2.addWidget(self.partsEdit)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.cur_part = QtWidgets.QLabel(self.centralwidget)
        self.cur_part.setObjectName("cur_part")
        self.horizontalLayout_2.addWidget(self.cur_part)
        self.partProgressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.partProgressBar.setProperty("value", 0)
        self.partProgressBar.setObjectName("partProgressBar")
        self.horizontalLayout_2.addWidget(self.partProgressBar)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.logBrowser = QtWidgets.QTextEdit(self.centralwidget)
        self.logBrowser.setObjectName("logBrowser")
        self.verticalLayout.addWidget(self.logBrowser)
        ExatronARB.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ExatronARB)
        self.statusbar.setObjectName("statusbar")
        ExatronARB.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(ExatronARB)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 811, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        ExatronARB.setMenuBar(self.menuBar)
        self.actionGogo = QtWidgets.QAction(ExatronARB)
        self.actionGogo.setObjectName("actionGogo")
        self.actionopen = QtWidgets.QAction(ExatronARB)
        self.actionopen.setObjectName("actionopen")
        self.actionsave = QtWidgets.QAction(ExatronARB)
        self.actionsave.setObjectName("actionsave")
        self.menuFile.addAction(self.actionopen)
        self.menuFile.addAction(self.actionsave)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(ExatronARB)
        QtCore.QMetaObject.connectSlotsByName(ExatronARB)

    def retranslateUi(self, ExatronARB):
        _translate = QtCore.QCoreApplication.translate
        ExatronARB.setWindowTitle(_translate("ExatronARB", "ExaJobLauncher"))
        self.connectButton.setText(_translate("ExatronARB", "Connect"))
        self.aboartButton.setText(_translate("ExatronARB", "Abort"))
        self.startButton.setText(_translate("ExatronARB", "Start"))
        self.label_5.setText(_translate("ExatronARB", "Bench Command"))
        self.cmdLineEdit.setText(_translate("ExatronARB", "arb_tester --fixed_temperature={temperature} --part_id=={part}"))
        self.label_2.setText(_translate("ExatronARB", "TEMP LIST"))
        self.tempEdit.setText(_translate("ExatronARB", "25,85,-40"))
        self.label_3.setText(_translate("ExatronARB", "Accuracy"))
        self.label_4.setText(_translate("ExatronARB", "Soak"))
        self.cur_temp.setText(_translate("ExatronARB", "25"))
        self.label.setText(_translate("ExatronARB", "PARTS LIST ##"))
        self.partsEdit.setText(_translate("ExatronARB", "1,2,3"))
        self.cur_part.setText(_translate("ExatronARB", "10"))
        self.menuFile.setTitle(_translate("ExatronARB", "File"))
        self.actionGogo.setText(_translate("ExatronARB", "gogo"))
        self.actionopen.setText(_translate("ExatronARB", "open"))
        self.actionsave.setText(_translate("ExatronARB", "save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ExatronARB = QtWidgets.QMainWindow()
    ui = Ui_ExatronARB()
    ui.setupUi(ExatronARB)
    ExatronARB.show()
    sys.exit(app.exec_())