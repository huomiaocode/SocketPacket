# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MsgIdList.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MsgIdList(object):
    def setupUi(self, MsgIdList):
        if not MsgIdList.objectName():
            MsgIdList.setObjectName(u"MsgIdList")
        MsgIdList.resize(617, 439)
        self.verticalLayout = QVBoxLayout(MsgIdList)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.msgIdList = QTableWidget(MsgIdList)
        if (self.msgIdList.columnCount() < 4):
            self.msgIdList.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.msgIdList.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.msgIdList.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.msgIdList.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.msgIdList.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.msgIdList.setObjectName(u"msgIdList")
        self.msgIdList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.msgIdList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.msgIdList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.msgIdList.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.msgIdList.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.msgIdList.horizontalHeader().setHighlightSections(False)
        self.msgIdList.horizontalHeader().setStretchLastSection(True)
        self.msgIdList.verticalHeader().setVisible(False)
        self.msgIdList.verticalHeader().setMinimumSectionSize(20)
        self.msgIdList.verticalHeader().setDefaultSectionSize(20)

        self.verticalLayout.addWidget(self.msgIdList)


        self.retranslateUi(MsgIdList)

        QMetaObject.connectSlotsByName(MsgIdList)
    # setupUi

    def retranslateUi(self, MsgIdList):
        MsgIdList.setWindowTitle(QCoreApplication.translate("MsgIdList", u"\u6d88\u606f\u8868", None))
        ___qtablewidgetitem = self.msgIdList.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MsgIdList", u"\u7aef\u53e3", None));
        ___qtablewidgetitem1 = self.msgIdList.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MsgIdList", u"\u6d88\u606fID", None));
        ___qtablewidgetitem2 = self.msgIdList.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MsgIdList", u"\u6d88\u606f\u540d\u79f0", None));
        ___qtablewidgetitem3 = self.msgIdList.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MsgIdList", u"PB\u540d\u79f0", None));
    # retranslateUi

