#-------------------------------------------------------------------------------
# Name:        breakBeats
# Purpose:     A SoundCloud-integrated music store simulation.
# Author:      Kenta Iwasaki
# Created:     08/03/2014
# Copyright:   (c) Kenta Iwasaki 2014
#-------------------------------------------------------------------------------

# PyQT Framework Module Imports
from PyQt5 import QtCore, QtGui, QtWidgets

# A layout container for the Manager Panel's context.
class Ui_ManagerPanel(object):
    # Initiates and defines all the GUI elements along with their properties.
    def setupUi(self, ManagerPanel):
        ManagerPanel.setObjectName("ManagerPanel")
        ManagerPanel.resize(400, 152)
        self.setList = QtWidgets.QListWidget(ManagerPanel)
        self.setList.setGeometry(QtCore.QRect(10, 50, 381, 91))
        self.setList.setObjectName("setList")
        self.horizontalLayoutWidget = QtWidgets.QWidget(ManagerPanel)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnAddSet = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnAddSet.setObjectName("btnAddSet")
        self.horizontalLayout.addWidget(self.btnAddSet)
        self.btnRemoveSet = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnRemoveSet.setObjectName("btnRemoveSet")
        self.horizontalLayout.addWidget(self.btnRemoveSet)

        self.retranslateUi(ManagerPanel)
        QtCore.QMetaObject.connectSlotsByName(ManagerPanel)

    # Set's string constant values for the UI elements.
    def retranslateUi(self, ManagerPanel):
        _translate = QtCore.QCoreApplication.translate
        ManagerPanel.setWindowTitle(_translate("ManagerPanel", "breakBeats :: Manager Panel"))
        self.btnAddSet.setText(_translate("ManagerPanel", "Add SoundCloud Set"))
        self.btnRemoveSet.setText(_translate("ManagerPanel", "Remove SoundCloud Set"))

