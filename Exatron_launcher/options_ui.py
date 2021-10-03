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
        options.resize(565, 405)
        self.verticalLayout = QtWidgets.QVBoxLayout(options)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(options)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(options)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(options)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit_2 = QtWidgets.QLineEdit(options)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.spinBox = QtWidgets.QSpinBox(options)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.pushButton = QtWidgets.QPushButton(options)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(options)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton_3 = QtWidgets.QPushButton(options)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)

        self.retranslateUi(options)
        QtCore.QMetaObject.connectSlotsByName(options)

    def retranslateUi(self, options):
        _translate = QtCore.QCoreApplication.translate
        options.setWindowTitle(_translate("options", "Dialog"))
        self.label_2.setText(_translate("options", "TextLabel"))
        self.label.setText(_translate("options", "TextLabel"))
        self.pushButton.setText(_translate("options", "PushButton"))
        self.pushButton_2.setText(_translate("options", "PushButton"))
        self.pushButton_3.setText(_translate("options", "PushButton"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    options = QtWidgets.QDialog()
    ui = Ui_options()
    ui.setupUi(options)
    options.show()
    sys.exit(app.exec_())
