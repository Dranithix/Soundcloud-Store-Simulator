#-------------------------------------------------------------------------------
# Name:        breakBeats
# Purpose:     A SoundCloud-integrated music store simulation.
# Author:      Kenta Iwasaki
# Created:     08/03/2014
# Copyright:   (c) Kenta Iwasaki 2014
#-------------------------------------------------------------------------------

# PyQT Framework Module Imports
from PyQt5 import QtCore, QtGui, QtWidgets

# A layout container for the Checkout Dialog's context.
class Ui_CheckoutDialog(object):
    # Initiates and defines all the GUI elements along with their properties.
    def setupUi(self, CheckoutDialog):
        CheckoutDialog.setObjectName("CheckoutDialog")
        CheckoutDialog.resize(711, 338)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CheckoutDialog.sizePolicy().hasHeightForWidth())
        CheckoutDialog.setSizePolicy(sizePolicy)
        CheckoutDialog.setMinimumSize(QtCore.QSize(711, 338))
        CheckoutDialog.setMaximumSize(QtCore.QSize(711, 338))
        self.orderList = QtWidgets.QTableWidget(CheckoutDialog)
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
        self.gridLayoutWidget = QtWidgets.QWidget(CheckoutDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 299, 141, 31))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.totalCost = QtWidgets.QLabel(self.gridLayoutWidget)
        self.totalCost.setObjectName("totalCost")
        self.gridLayout.addWidget(self.totalCost, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(CheckoutDialog)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(450, 300, 251, 31))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btnRemoveTrack = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btnRemoveTrack.setObjectName("btnRemoveTrack")
        self.gridLayout_2.addWidget(self.btnRemoveTrack, 0, 0, 1, 1)
        self.btnPurchase = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btnPurchase.setObjectName("btnPurchase")
        self.gridLayout_2.addWidget(self.btnPurchase, 0, 2, 1, 1)
        self.btnEmptyCart = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btnEmptyCart.setObjectName("btnEmptyCart")
        self.gridLayout_2.addWidget(self.btnEmptyCart, 0, 1, 1, 1)

        self.retranslateUi(CheckoutDialog)
        QtCore.QMetaObject.connectSlotsByName(CheckoutDialog)

    # Set's string constant values for the UI elements.
    def retranslateUi(self, CheckoutDialog):
        _translate = QtCore.QCoreApplication.translate
        CheckoutDialog.setWindowTitle(_translate("CheckoutDialog", "breakBeats :: Checkout"))
        self.orderList.setSortingEnabled(True)
        item = self.orderList.horizontalHeaderItem(1)
        item.setText(_translate("CheckoutDialog", "Title"))
        item = self.orderList.horizontalHeaderItem(2)
        item.setText(_translate("CheckoutDialog", "Duration"))
        item = self.orderList.horizontalHeaderItem(3)
        item.setText(_translate("CheckoutDialog", "Artist"))
        item = self.orderList.horizontalHeaderItem(4)
        item.setText(_translate("CheckoutDialog", "Price"))
        self.totalCost.setText(_translate("CheckoutDialog", "0"))
        self.label.setText(_translate("CheckoutDialog", "Total Cost:"))
        self.btnRemoveTrack.setText(_translate("CheckoutDialog", "Delete Track"))
        self.btnPurchase.setText(_translate("CheckoutDialog", "Purchase"))
        self.btnEmptyCart.setText(_translate("CheckoutDialog", "Empty Cart"))

