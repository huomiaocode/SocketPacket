# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CardSetWin.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_CardSetWin(object):
    def setupUi(self, CardSetWin):
        if not CardSetWin.objectName():
            CardSetWin.setObjectName(u"CardSetWin")
        CardSetWin.setWindowModality(Qt.ApplicationModal)
        CardSetWin.resize(323, 105)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CardSetWin.sizePolicy().hasHeightForWidth())
        CardSetWin.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(CardSetWin)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(CardSetWin)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.netcardCb = QComboBox(CardSetWin)
        self.netcardCb.setObjectName(u"netcardCb")

        self.verticalLayout.addWidget(self.netcardCb)

        self.label_2 = QLabel(CardSetWin)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.modeCb = QComboBox(CardSetWin)
        self.modeCb.addItem("")
        self.modeCb.addItem("")
        self.modeCb.setObjectName(u"modeCb")
        self.modeCb.setMinimumSize(QSize(80, 0))

        self.horizontalLayout.addWidget(self.modeCb)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.confirmBtn = QPushButton(CardSetWin)
        self.confirmBtn.setObjectName(u"confirmBtn")

        self.horizontalLayout.addWidget(self.confirmBtn)

        self.cancelBtn = QPushButton(CardSetWin)
        self.cancelBtn.setObjectName(u"cancelBtn")

        self.horizontalLayout.addWidget(self.cancelBtn)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(CardSetWin)

        QMetaObject.connectSlotsByName(CardSetWin)
    # setupUi

    def retranslateUi(self, CardSetWin):
        CardSetWin.setWindowTitle(QCoreApplication.translate("CardSetWin", u"\u9009\u62e9\u7f51\u5361\u53ca\u6253\u5f00\u6a21\u5f0f", None))
        self.label.setText(QCoreApplication.translate("CardSetWin", u"\u9009\u62e9\u8981\u76d1\u89c6\u7684\u7f51\u5361", None))
        self.label_2.setText(QCoreApplication.translate("CardSetWin", u"\u9009\u62e9\u6253\u5f00\u6a21\u5f0f", None))
        self.modeCb.setItemText(0, QCoreApplication.translate("CardSetWin", u"\u76f4\u63a5\u6a21\u5f0f", None))
        self.modeCb.setItemText(1, QCoreApplication.translate("CardSetWin", u"\u6df7\u6742\u6a21\u5f0f", None))

        self.confirmBtn.setText(QCoreApplication.translate("CardSetWin", u"\u786e\u5b9a", None))
        self.cancelBtn.setText(QCoreApplication.translate("CardSetWin", u"\u53d6\u6d88", None))
    # retranslateUi

