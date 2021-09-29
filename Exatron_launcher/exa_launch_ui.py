# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'exa_launch_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ExaJobLauncher(object):
    def setupUi(self, ExaJobLauncher):
        ExaJobLauncher.setObjectName("ExaJobLauncher")
        ExaJobLauncher.resize(811, 555)
        ExaJobLauncher.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(ExaJobLauncher)
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
        self.abortButton = QtWidgets.QPushButton(self.centralwidget)
        self.abortButton.setObjectName("abortButton")
        self.horizontalLayout_3.addWidget(self.abortButton)
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setEnabled(True)
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
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.tempSoakSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.tempSoakSpinBox.setMinimum(1)
        self.tempSoakSpinBox.setSingleStep(10)
        self.tempSoakSpinBox.setObjectName("tempSoakSpinBox")
        self.horizontalLayout.addWidget(self.tempSoakSpinBox)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
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
        ExaJobLauncher.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ExaJobLauncher)
        self.statusbar.setObjectName("statusbar")
        ExaJobLauncher.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(ExaJobLauncher)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 811, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuoptions = QtWidgets.QMenu(self.menuBar)
        self.menuoptions.setObjectName("menuoptions")
        ExaJobLauncher.setMenuBar(self.menuBar)
        self.actionGogo = QtWidgets.QAction(ExaJobLauncher)
        self.actionGogo.setObjectName("actionGogo")
        self.actionopen = QtWidgets.QAction(ExaJobLauncher)
        self.actionopen.setObjectName("actionopen")
        self.actionsave = QtWidgets.QAction(ExaJobLauncher)
        self.actionsave.setObjectName("actionsave")
        self.actiondebug = QtWidgets.QAction(ExaJobLauncher)
        self.actiondebug.setObjectName("actiondebug")
        self.menuFile.addAction(self.actionopen)
        self.menuFile.addAction(self.actionsave)
        self.menuoptions.addAction(self.actiondebug)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuoptions.menuAction())

        self.retranslateUi(ExaJobLauncher)
        QtCore.QMetaObject.connectSlotsByName(ExaJobLauncher)

    def retranslateUi(self, ExaJobLauncher):
        _translate = QtCore.QCoreApplication.translate
        ExaJobLauncher.setWindowTitle(_translate("ExaJobLauncher", "ExaJobLauncher"))
        self.connectButton.setText(_translate("ExaJobLauncher", "Connect"))
        self.abortButton.setText(_translate("ExaJobLauncher", "Abort"))
        self.startButton.setText(_translate("ExaJobLauncher", "Start"))
        self.label_5.setText(_translate("ExaJobLauncher", "Bench Command"))
        self.cmdLineEdit.setText(_translate("ExaJobLauncher", "arb_tester --fixed_temperature={temperature} --part_id=={part}"))
        self.label_2.setText(_translate("ExaJobLauncher", "TEMP LIST"))
        self.tempEdit.setText(_translate("ExaJobLauncher", "25,85,-40"))
        self.label_4.setText(_translate("ExaJobLauncher", "Soak"))
        self.label_3.setText(_translate("ExaJobLauncher", "Accuracy"))
        self.cur_temp.setText(_translate("ExaJobLauncher", "25"))
        self.label.setText(_translate("ExaJobLauncher", "PARTS LIST ##"))
        self.partsEdit.setText(_translate("ExaJobLauncher", "1,2,3"))
        self.cur_part.setText(_translate("ExaJobLauncher", "10"))
        self.menuFile.setTitle(_translate("ExaJobLauncher", "File"))
        self.menuoptions.setTitle(_translate("ExaJobLauncher", "options"))
        self.actionGogo.setText(_translate("ExaJobLauncher", "gogo"))
        self.actionopen.setText(_translate("ExaJobLauncher", "open"))
        self.actionsave.setText(_translate("ExaJobLauncher", "save"))
        self.actiondebug.setText(_translate("ExaJobLauncher", "debug"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ExaJobLauncher = QtWidgets.QMainWindow()
    ui = Ui_ExaJobLauncher()
    ui.setupUi(ExaJobLauncher)
    ExaJobLauncher.show()
    sys.exit(app.exec_())
