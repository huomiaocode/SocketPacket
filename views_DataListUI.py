# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DataList.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DataList(object):
    def setupUi(self, DataList):
        if not DataList.objectName():
            DataList.setObjectName(u"DataList")
        DataList.resize(400, 300)
        self.verticalLayout = QVBoxLayout(DataList)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 0, 5)
        self.tableView = QTableView(DataList)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setStyleSheet(u"selection-background-color: rgb(0, 120, 215);\n"
"selection-color: rgb(255, 255, 255);")
        self.tableView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableView.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.verticalHeader().setMinimumSectionSize(20)
        self.tableView.verticalHeader().setDefaultSectionSize(20)

        self.verticalLayout.addWidget(self.tableView)


        self.retranslateUi(DataList)

        QMetaObject.connectSlotsByName(DataList)
    # setupUi

    def retranslateUi(self, DataList):
        DataList.setWindowTitle(QCoreApplication.translate("DataList", u"DataList", None))
    # retranslateUi

