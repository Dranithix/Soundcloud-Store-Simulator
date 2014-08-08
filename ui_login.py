#-------------------------------------------------------------------------------
# Name:        breakBeats
# Purpose:     A SoundCloud-integrated music store simulation.
# Author:      Kenta Iwasaki
# Created:     08/03/2014
# Copyright:   (c) Kenta Iwasaki 2014
#-------------------------------------------------------------------------------

# PyQT Framework Module Imports
from PyQt5 import QtCore, QtGui, QtWidgets

# A layout container for the Login Dialog's context.
class Ui_LoginDialog(object):
    # Initiates and defines all the GUI elements along with their properties.
    def setupUi(self, LoginDialog):
        LoginDialog.setObjectName("LoginDialog")
        LoginDialog.resize(390, 99)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LoginDialog.sizePolicy().hasHeightForWidth())
        LoginDialog.setSizePolicy(sizePolicy)
        LoginDialog.setMinimumSize(QtCore.QSize(390, 99))
        LoginDialog.setMaximumSize(QtCore.QSize(390, 99))
        self.gridLayoutWidget = QtWidgets.QWidget(LoginDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 371, 81))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.btnLogin = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnLogin.setObjectName("btnLogin")
        self.gridLayout.addWidget(self.btnLogin, 2, 2, 1, 1)
        self.btnRegister = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnRegister.setObjectName("btnRegister")
        self.gridLayout.addWidget(self.btnRegister, 2, 3, 1, 1)
        self.txtPassword = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.txtPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txtPassword.setObjectName("txtPassword")
        self.gridLayout.addWidget(self.txtPassword, 1, 1, 1, 3)
        self.txtUsername = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.txtUsername.setObjectName("txtUsername")
        self.gridLayout.addWidget(self.txtUsername, 0, 1, 1, 3)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 2)

        self.retranslateUi(LoginDialog)
        QtCore.QMetaObject.connectSlotsByName(LoginDialog)

    # Set's string constant values for the UI elements.
    def retranslateUi(self, LoginDialog):
        _translate = QtCore.QCoreApplication.translate
        LoginDialog.setWindowTitle(_translate("LoginDialog", "breakBeats :: Login"))
        self.label_2.setText(_translate("LoginDialog", "Password:"))
        self.label.setText(_translate("LoginDialog", "Username:"))
        self.btnLogin.setText(_translate("LoginDialog", "Login"))
        self.btnRegister.setText(_translate("LoginDialog", "Register"))
        self.label_3.setText(_translate("LoginDialog", "Welcome to breakBeats v0.1"))

