# -*- coding:utf8 -*-

from PySide2.QtWidgets import QApplication, QMessageBox, QWidget
from PySide2.QtGui import QIcon

import ctypes
import ctypes.util
import sys

try:
    if sys.platform.startswith('win'):
        _lib = ctypes.CDLL('wpcap.dll')
    else:
        _lib = ctypes.CDLL(ctypes.util.find_library('pcap'))
    del _lib
except:
    app = QApplication(sys.argv)
    QMessageBox.information(None, "提示", "你需要安装pcap类库！")
    sys.exit()

import views
from views_SocketPacketMainUI import Ui_SocketPacketMain
from views_DataList import DataList
import Res # 不能删


class TexaspokerMain(QWidget):
    """
    数据查看器，主程序
    """

    def __init__(self):
        super().__init__()

        self.ui = Ui_SocketPacketMain()
        self.ui.setupUi(self)

        self.initViews()

    def initViews(self):
        self.setMinimumWidth(1200)

        self.lList = DataList()
        self.rPanel = views.ControlsPanel()

        self.ui.leftLayout.addWidget(self.lList)
        self.ui.rightLayout.addWidget(self.rPanel)

        self.lList.setDetailTextCallback(self.rPanel.setDetailText)
        self.rPanel.setDataCallback(self.lList.onData)
        self.rPanel.setOnDataFormatChanged(self.lList.onDataFormatChanged)
        self.rPanel.setOnReParseBuff(self.lList.onReParseBuff)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":icon.ico"))
    main = TexaspokerMain()
    main.show()
    print("app run!")
    sys.exit(app.exec_())
