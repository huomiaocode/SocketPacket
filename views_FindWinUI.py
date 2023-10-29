# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FindWin.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_FindWin(object):
    def setupUi(self, FindWin):
        if not FindWin.objectName():
            FindWin.setObjectName(u"FindWin")
        FindWin.resize(341, 101)
        FindWin.setMinimumSize(QSize(0, 100))
        FindWin.setMaximumSize(QSize(16777215, 101))
        self.verticalLayout = QVBoxLayout(FindWin)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(FindWin)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.findTxt = QLineEdit(FindWin)
        self.findTxt.setObjectName(u"findTxt")

        self.horizontalLayout.addWidget(self.findTxt)

        self.findBtn = QPushButton(FindWin)
        self.findBtn.setObjectName(u"findBtn")
        self.findBtn.setMinimumSize(QSize(80, 0))
        self.findBtn.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.findBtn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.upCaseCb = QCheckBox(FindWin)
        self.upCaseCb.setObjectName(u"upCaseCb")

        self.horizontalLayout_2.addWidget(self.upCaseCb)

        self.groupBox = QGroupBox(FindWin)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(140, 50))
        self.groupBox.setMaximumSize(QSize(140, 50))
        self.upRb = QRadioButton(self.groupBox)
        self.upRb.setObjectName(u"upRb")
        self.upRb.setGeometry(QRect(20, 20, 51, 16))
        self.downRb = QRadioButton(self.groupBox)
        self.downRb.setObjectName(u"downRb")
        self.downRb.setGeometry(QRect(80, 20, 51, 16))
        self.downRb.setChecked(True)

        self.horizontalLayout_2.addWidget(self.groupBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.cancelBtn = QPushButton(FindWin)
        self.cancelBtn.setObjectName(u"cancelBtn")
        self.cancelBtn.setMinimumSize(QSize(80, 0))
        self.cancelBtn.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_2.addWidget(self.cancelBtn, 0, Qt.AlignTop)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(FindWin)

        QMetaObject.connectSlotsByName(FindWin)
    # setupUi

    def retranslateUi(self, FindWin):
        FindWin.setWindowTitle(QCoreApplication.translate("FindWin", u"\u67e5\u627e", None))
        self.label.setText(QCoreApplication.translate("FindWin", u"\u67e5\u627e\u5185\u5bb9\uff1a", None))
        self.findBtn.setText(QCoreApplication.translate("FindWin", u"\u67e5\u627e", None))
        self.upCaseCb.setText(QCoreApplication.translate("FindWin", u"\u533a\u5206\u5927\u5c0f\u5199", None))
        self.groupBox.setTitle(QCoreApplication.translate("FindWin", u"\u65b9\u5411", None))
        self.upRb.setText(QCoreApplication.translate("FindWin", u"\u5411\u4e0a", None))
        self.downRb.setText(QCoreApplication.translate("FindWin", u"\u5411\u4e0b", None))
        self.cancelBtn.setText(QCoreApplication.translate("FindWin", u"\u53d6\u6d88", None))
    # retranslateUi

