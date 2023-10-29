# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProtobufTree.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ProtobufTree(object):
    def setupUi(self, ProtobufTree):
        if not ProtobufTree.objectName():
            ProtobufTree.setObjectName(u"ProtobufTree")
        ProtobufTree.resize(357, 467)
        self.verticalLayout = QVBoxLayout(ProtobufTree)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.treeWidget = QTreeWidget(ProtobufTree)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.header().setVisible(False)

        self.verticalLayout.addWidget(self.treeWidget)


        self.retranslateUi(ProtobufTree)

        QMetaObject.connectSlotsByName(ProtobufTree)
    # setupUi

    def retranslateUi(self, ProtobufTree):
        ProtobufTree.setWindowTitle(QCoreApplication.translate("ProtobufTree", u"\u534f\u8bae\u6811", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("ProtobufTree", u"\u6570\u636e", None));
    # retranslateUi

