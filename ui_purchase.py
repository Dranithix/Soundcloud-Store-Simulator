#-------------------------------------------------------------------------------
# Name:        breakBeats
# Purpose:     A SoundCloud-integrated music store simulation.
# Author:      Kenta Iwasaki
# Created:     08/03/2014
# Copyright:   (c) Kenta Iwasaki 2014
#-------------------------------------------------------------------------------

# PyQT Framework Module Imports
from PyQt5 import QtCore, QtGui, QtWidgets

# A layout container for the Purchase History's context.
class Ui_PurchaseHistory(object):
    # Initiates and defines all the GUI elements along with their properties.
    def setupUi(self, PurchaseHistory):
        PurchaseHistory.setObjectName("PurchaseHistory")
        PurchaseHistory.resize(711, 341)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PurchaseHistory.sizePolicy().hasHeightForWidth())
        PurchaseHistory.setSizePolicy(sizePolicy)
        PurchaseHistory.setMinimumSize(QtCore.QSize(711, 341))
        PurchaseHistory.setMaximumSize(QtCore.QSize(711, 341))
        self.gridLayoutWidget_2 = QtWidgets.QWidget(PurchaseHistory)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(530, 300, 171, 31))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btnDownload = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btnDownload.setObjectName("btnDownload")
        self.gridLayout_2.addWidget(self.btnDownload, 0, 0, 1, 1)
        self.orderList = QtWidgets.QTableWidget(PurchaseHistory)
        self.orderList.setGeometry(QtCore.QRect(10, 10, 691, 281))
        self.orderList.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.orderList.setAcceptDrops(False)
        self.orderList.setAutoFillBackground(False)
        self.orderList.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.orderList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.orderList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.orderList.setShowGrid(True)
        self.orderList.setCornerButtonEnabled(False)
        self.orderList.setObjectName("orderList")
        self.orderList.setColumnCount(5)
        self.orderList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.orderList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.orderList.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.orderList.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.orderList.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.orderList.setHorizontalHeaderItem(4, item)
        self.orderList.horizontalHeader().setStretchLastSection(True)
        self.orderList.verticalHeader().setCascadingSectionResizes(True)
        self.orderList.verticalHeader().setDefaultSectionSize(64)
        self.orderList.verticalHeader().setMinimumSectionSize(64)
        self.orderList.verticalHeader().setStretchLastSection(False)

        self.retranslateUi(PurchaseHistory)
        QtCore.QMetaObject.connectSlotsByName(PurchaseHistory)

    # Set's string constant values for the UI elements.
    def retranslateUi(self, PurchaseHistory):
        _translate = QtCore.QCoreApplication.translate
        PurchaseHistory.setWindowTitle(_translate("PurchaseHistory", "breakBeats :: Purchase History"))
        self.btnDownload.setText(_translate("PurchaseHistory", "Download Track"))
        self.orderList.setSortingEnabled(True)
        item = self.orderList.horizontalHeaderItem(1)
        item.setText(_translate("PurchaseHistory", "Title"))
        item = self.orderList.horizontalHeaderItem(2)
        item.setText(_translate("PurchaseHistory", "Duration"))
        item = self.orderList.horizontalHeaderItem(3)
        item.setText(_translate("PurchaseHistory", "Artist"))
        item = self.orderList.horizontalHeaderItem(4)
        item.setText(_translate("PurchaseHistory", "Price"))

