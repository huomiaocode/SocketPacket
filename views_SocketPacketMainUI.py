# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SocketPacketMain.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_SocketPacketMain(object):
    def setupUi(self, SocketPacketMain):
        if not SocketPacketMain.objectName():
            SocketPacketMain.setObjectName(u"SocketPacketMain")
        SocketPacketMain.resize(665, 536)
        self.horizontalLayout = QHBoxLayout(SocketPacketMain)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(SocketPacketMain)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.leftLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.leftLayout.setObjectName(u"leftLayout")
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.rightLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.rightLayout.setSpacing(0)
        self.rightLayout.setObjectName(u"rightLayout")
        self.rightLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter.addWidget(self.verticalLayoutWidget_2)

        self.horizontalLayout.addWidget(self.splitter)


        self.retranslateUi(SocketPacketMain)

        QMetaObject.connectSlotsByName(SocketPacketMain)
    # setupUi

    def retranslateUi(self, SocketPacketMain):
        SocketPacketMain.setWindowTitle(QCoreApplication.translate("SocketPacketMain", u"\u534f\u8bae\u6570\u636e\u5206\u6790\u5de5\u5177", None))
    # retranslateUi

