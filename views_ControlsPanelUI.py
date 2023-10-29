# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ControlsPanel.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ControlsPanel(object):
    def setupUi(self, ControlsPanel):
        if not ControlsPanel.objectName():
            ControlsPanel.setObjectName(u"ControlsPanel")
        ControlsPanel.resize(496, 414)
        self.verticalLayout = QVBoxLayout(ControlsPanel)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 5, 5, 5)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_2 = QWidget(ControlsPanel)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QSize(75, 0))
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.protobufTreeBtn = QPushButton(self.widget_2)
        self.protobufTreeBtn.setObjectName(u"protobufTreeBtn")
        sizePolicy.setHeightForWidth(self.protobufTreeBtn.sizePolicy().hasHeightForWidth())
        self.protobufTreeBtn.setSizePolicy(sizePolicy)
        self.protobufTreeBtn.setMinimumSize(QSize(75, 30))

        self.verticalLayout_3.addWidget(self.protobufTreeBtn)

        self.msgIdBtn = QPushButton(self.widget_2)
        self.msgIdBtn.setObjectName(u"msgIdBtn")
        sizePolicy.setHeightForWidth(self.msgIdBtn.sizePolicy().hasHeightForWidth())
        self.msgIdBtn.setSizePolicy(sizePolicy)
        self.msgIdBtn.setMinimumSize(QSize(75, 30))

        self.verticalLayout_3.addWidget(self.msgIdBtn)

        self.cardsetBtn = QPushButton(self.widget_2)
        self.cardsetBtn.setObjectName(u"cardsetBtn")
        sizePolicy.setHeightForWidth(self.cardsetBtn.sizePolicy().hasHeightForWidth())
        self.cardsetBtn.setSizePolicy(sizePolicy)
        self.cardsetBtn.setMinimumSize(QSize(75, 30))

        self.verticalLayout_3.addWidget(self.cardsetBtn)


        self.horizontalLayout.addWidget(self.widget_2)

        self.ipContainer = QWidget(ControlsPanel)
        self.ipContainer.setObjectName(u"ipContainer")
        self.ipContainer.setMinimumSize(QSize(300, 0))
        self.ipContainerLayout = QVBoxLayout(self.ipContainer)
        self.ipContainerLayout.setSpacing(3)
        self.ipContainerLayout.setObjectName(u"ipContainerLayout")
        self.ipContainerLayout.setContentsMargins(5, 5, 5, 5)

        self.horizontalLayout.addWidget(self.ipContainer, 0, Qt.AlignTop)

        self.frame = QFrame(ControlsPanel)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(80, 0))
        self.frame.setMaximumSize(QSize(80, 16777215))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.processBtn = QPushButton(self.frame)
        self.processBtn.setObjectName(u"processBtn")
        sizePolicy.setHeightForWidth(self.processBtn.sizePolicy().hasHeightForWidth())
        self.processBtn.setSizePolicy(sizePolicy)
        self.processBtn.setMinimumSize(QSize(80, 30))

        self.verticalLayout_2.addWidget(self.processBtn)

        self.filterBtn = QPushButton(self.frame)
        self.filterBtn.setObjectName(u"filterBtn")
        sizePolicy.setHeightForWidth(self.filterBtn.sizePolicy().hasHeightForWidth())
        self.filterBtn.setSizePolicy(sizePolicy)
        self.filterBtn.setMinimumSize(QSize(80, 30))

        self.verticalLayout_2.addWidget(self.filterBtn)

        self.startBtn = QPushButton(self.frame)
        self.startBtn.setObjectName(u"startBtn")
        sizePolicy.setHeightForWidth(self.startBtn.sizePolicy().hasHeightForWidth())
        self.startBtn.setSizePolicy(sizePolicy)
        self.startBtn.setMinimumSize(QSize(80, 30))

        self.verticalLayout_2.addWidget(self.startBtn)


        self.horizontalLayout.addWidget(self.frame)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.detailTxt = QTextEdit(ControlsPanel)
        self.detailTxt.setObjectName(u"detailTxt")

        self.verticalLayout.addWidget(self.detailTxt)


        self.retranslateUi(ControlsPanel)

        QMetaObject.connectSlotsByName(ControlsPanel)
    # setupUi

    def retranslateUi(self, ControlsPanel):
        ControlsPanel.setWindowTitle(QCoreApplication.translate("ControlsPanel", u"ControlsPanel", None))
        self.protobufTreeBtn.setText(QCoreApplication.translate("ControlsPanel", u"\u534f\u8bae\u6811", None))
        self.msgIdBtn.setText(QCoreApplication.translate("ControlsPanel", u"\u6d88\u606f\u8868", None))
        self.cardsetBtn.setText(QCoreApplication.translate("ControlsPanel", u"\u7f51\u5361\u8bbe\u7f6e", None))
        self.processBtn.setText(QCoreApplication.translate("ControlsPanel", u"\u6240\u6709\u8fdb\u7a0b", None))
        self.filterBtn.setText(QCoreApplication.translate("ControlsPanel", u"\u8fc7\u6ee4", None))
        self.startBtn.setText(QCoreApplication.translate("ControlsPanel", u"\u542f\u52a8", None))
    # retranslateUi

