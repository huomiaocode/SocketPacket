# -*- coding:utf8 -*-

import sys
from PySide2.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QTreeWidgetItem, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy, QAction, QMenu, QActionGroup
from PySide2.QtCore import Qt, QEvent
from PySide2.QtGui import QColor, QIcon, QCursor
from winpcapy import *
from views_CardSetWinUI import Ui_CardSetWin
from views_ProtobufTreeUI import Ui_ProtobufTree
from views_MsgIdListUI import Ui_MsgIdList
from views_ControlsPanelUI import Ui_ControlsPanel
from views_FindWinUI import Ui_FindWin
import fetchDataPcap
from datas import appData
import GenerateData
import Res # 不能删

class ControlsPanel(QWidget):
    '''
    这个是程序右上方的按钮和文本框
    '''

    processPid = None

    def __init__(self):
        super().__init__()

        self.ui = Ui_ControlsPanel()
        self.ui.setupUi(self)

        flags = Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint
        self.setWindowFlags(flags)

        self.protobufTree = None
        self.msgIdListUI = None
        self.cardSetWin = None

        self.isRunning = False
        self.filterStr = ""
        self.threadE = None
        self.dataCallback = None
        self.processPid = None
        self.adhandle = None
        self.enabledArr = []
        self.inputTxtArr = []

        self.selectedName = ""
        self.selectedMode = 0

        self.onDataFormatChanged = None
        self.onReParseBuff = None

        self.initViews()
        self.addMenus()

        self.ui.processBtn.setIcon(QIcon(":target.png"))

        self.ui.protobufTreeBtn.clicked.connect(self.onClickProtobufTreeBtn)
        self.ui.msgIdBtn.clicked.connect(self.onClickMsgIdBtn)
        self.ui.cardsetBtn.clicked.connect(self.onClickCardSetBtn)
        self.ui.filterBtn.clicked.connect(self.onFilter)
        self.ui.startBtn.clicked.connect(self.onStartUp)

        self.ui.processBtn.installEventFilter(self)
    
    def initViews(self):
        self.setMinimumWidth(380)

        self.ui.filterBtn.setEnabled(False)
        self.ui.startBtn.setEnabled(False)

        self.enabledArr = []
        self.inputTxtArr = []

        pDataLen = len(GenerateData.ProtobufData)
        for i in range(pDataLen):
            pData = GenerateData.ProtobufData[i]
            layout = QHBoxLayout(self.ui.ipContainer)
            layout.setSpacing(3)
            layout.setContentsMargins(0, 0, 0, 0)
            self.ui.ipContainerLayout.addLayout(layout)

            ipTxt = self.getLineEdit(layout, 100, pData["ip"])
            portTxt = self.getLineEdit(layout, 50, pData["port"])
            headlenTxt = self.getLineEdit(layout, 25, pData["headlen"])
            headlenTxt.setAlignment(Qt.AlignCenter)
            endianTxt = self.getLineEdit(layout, 20, pData["endian"])
            endianTxt.setAlignment(Qt.AlignCenter)
            layout.addItem(QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
            
            txtTuple = (ipTxt, portTxt, headlenTxt, endianTxt)
            self.inputTxtArr.append(txtTuple)
            self.enabledArr.extend(txtTuple)
            
        # self.enabledArr.append(self.wsCb)
        self.enabledArr.append(self.ui.filterBtn)
        self.enabledArr.append(self.ui.cardsetBtn)
        self.enabledArr.append(self.ui.processBtn)

    def addMenus(self):
        self.ui.detailTxt.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.detailTxt.customContextMenuRequested.connect(self.onCustomContextMenuRequested)

        self.textEditMenu = QMenu(self)
        dataFormatMenu = QMenu("数据 - 格式", self)
        reParseBuffMenu = QAction("重新解析", self)
        reParseBuffMenu.triggered.connect(self.onMenuReParseBuff)
        self.textEditMenu.addMenu(dataFormatMenu)
        self.textEditMenu.addAction(reParseBuffMenu)

        group = QActionGroup(self)
        actions = (
            QAction("字节流", self),
            QAction("十进制", self),
            QAction("十六进制", self)
        )
        for action in actions:
            action.setCheckable(True)
            action.setActionGroup(group)
        actions[appData.dataFormat].setChecked(True)
        group.triggered.connect(self.onMenuGroupTrigged)

        dataFormatMenu.addActions(actions)

    def onCustomContextMenuRequested(self):
        self.textEditMenu.exec_(QCursor.pos())

    def onMenuGroupTrigged(self, action:QAction):
        appData.dataFormat = action.actionGroup().actions().index(action)
        if self.onDataFormatChanged != None:
            self.onDataFormatChanged()

    def onMenuReParseBuff(self):
        if self.onReParseBuff != None:
            self.onReParseBuff()

    def getLineEdit(self, layout: QHBoxLayout, width, text):
        txt = QLineEdit(self.ui.ipContainer)
        txt.setFixedSize(width, 22)
        txt.setText(text)
        layout.addWidget(txt)
        return txt

    def eventFilter(self, widget, event):
        if widget == self.ui.processBtn:
            if self.ui.processBtn.isEnabled():
                if event.type() == QEvent.MouseButtonRelease:
                    if event.button() == Qt.RightButton:
                        self.ui.processBtn.setText("所有进程")
                        self.processPid = None
                        if self.threadE:
                            self.threadE.setProcessPid(self.processPid)
                    else:
                        self.onPickingProcess()
                        if self.threadE:
                            self.threadE.setProcessPid(self.processPid)
                    return True
        return QWidget.eventFilter(self, widget, event)

    def onPickingProcess(self):
        try:
            import win32gui, win32process		
            
            cursorPos = win32gui.GetCursorPos()
            hwnd = win32gui.WindowFromPoint(cursorPos)
            pid = repr(win32process.GetWindowThreadProcessId(hwnd)[1])
            self.ui.processBtn.setText(pid)
            self.processPid = pid
        except:
            QMessageBox.information(None, "提示", "你需要安装pywin32模块")
            pass
    
    def setDetailText(self, txt):
        self.ui.detailTxt.setText(txt)

    def setOnDataFormatChanged(self, onDataFormatChanged):
        self.onDataFormatChanged = onDataFormatChanged

    def setOnReParseBuff(self, onReParseBuff):
        self.onReParseBuff = onReParseBuff

    def onClickProtobufTreeBtn(self):
        if self.protobufTree == None:
            self.protobufTree = ProtobufTree()
            def onDestroyed():
                self.protobufTree = None
            self.protobufTree.destroyed.connect(onDestroyed)
        self.protobufTree.show()
        self.protobufTree.raise_()

    def onClickMsgIdBtn(self):
        if self.msgIdListUI == None:
            self.msgIdListUI = MsgIdListUI()
            def onDestroyed():
                self.msgIdListUI = None
            self.msgIdListUI.destroyed.connect(onDestroyed)
        self.msgIdListUI.show()
        self.msgIdListUI.raise_()

    def onClickCardSetBtn(self):
        if self.cardSetWin == None:
            self.cardSetWin = CardSetWin()
            def onDestroyed():
                self.cardSetWin = None
            self.cardSetWin.destroyed.connect(onDestroyed)

        def onCardSetCallback():
            self.selectedName = self.cardSetWin.selectedName
            self.selectedMode = self.cardSetWin.selectedMode
            self.ui.filterBtn.setEnabled(True)

        self.cardSetWin.setCallback(onCardSetCallback)
        self.cardSetWin.show()
        self.cardSetWin.raise_()

    def onFilter(self):
        self.filterStr = ""
        
        for i in range(len(self.inputTxtArr)):
            ip = self.inputTxtArr[i][0].text()
            port = self.inputTxtArr[i][1].text()
            headlen = self.inputTxtArr[i][2].text()
            endian = self.inputTxtArr[i][3].text()

            pData = None
            if i < len(GenerateData.ProtobufData):
                pData = GenerateData.ProtobufData[i]
            if not pData:
                continue
            
            pData["ip"] = ip
            pData["port"] = port
            pData["headlen"] = headlen
            pData["endian"] = endian
            
            ipPortStr = ""
            hasIp = False
            if ip!="*" and ip!="":
                hasIp = True
                ipPortStr = "src net %s" % ip
            if port!="*" and port!="":
                if hasIp:
                    ipPortStr += " and "
                ipPortStr += "tcp port %s" % port
            if self.filterStr != "":
                self.filterStr += " or "
            if ipPortStr!="":
                self.filterStr += "(%s)" % ipPortStr
        
        self.ui.startBtn.setEnabled(True)

    def onStartUp(self):
        if not self.isRunning:
            adhandle = self.getHandle()
            if not adhandle:
                QMessageBox.information(None, "提示", "获取pcap句柄为空！")
                return
            
            self.isRunning = True
            self.threadE = fetchDataPcap.FetchDataThread(adhandle, False) #, self.wsCb.IsChecked())
            self.threadE.setProcessPid(self.processPid)
            self.threadE.onPacket.connect(self.dataCallback)
            self.threadE.start()
            
            self.ui.startBtn.setText("暂停")
            for obj in self.enabledArr:
                obj.setEnabled(False)
        else:
            self.isRunning = False
            self.threadE.onPacket.disconnect(self.dataCallback)
            self.threadE.Close()
            self.threadE.quit()
            self.threadE.wait()
            self.threadE = None
            
            self.ui.startBtn.setText("启动")
            for obj in self.enabledArr:
                obj.setEnabled(True)

    def getHandle(self):
        errbuf = create_string_buffer(PCAP_ERRBUF_SIZE)
        adhandle = pcap_open_live(self.selectedName, 65536, self.selectedMode, 1000, errbuf)				

        fcode = bpf_program()
        if pcap_compile(adhandle, byref(fcode), self.filterStr.encode("utf-8"), 1, 0) < 0:
            QMessageBox.information(None, "提示", "编译出错，语法不正确。")
            pcap_close(adhandle)
       
        if pcap_setfilter(adhandle, byref(fcode)) < 0:
            QMessageBox.information(None, "提示", "设置filter时出错！")
            pcap_close(adhandle)
            
        return adhandle

    def setDataCallback(self, callback):
        self.dataCallback = callback

class CardSetWin(QWidget):

    def __init__(self):
        super().__init__()

        self.ui = Ui_CardSetWin()
        self.ui.setupUi(self)

        flags = Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.initViews()

        self.callback = None

        self.ui.confirmBtn.clicked.connect(self.onClickConfirmBtn)
        self.ui.cancelBtn.clicked.connect(self.onClickCancelBtn)

    def initViews(self):
        self.dNameArr = []
        self.dDescriptionArr = []
        self.selectedName = None
        self.selectedMode = 0

        errbuf = create_string_buffer(PCAP_ERRBUF_SIZE)
        alldevs = POINTER(pcap_if_t)()
        
        if pcap_findalldevs(byref(alldevs), errbuf) == -1:
            QMessageBox.information(None, "提示", "Error in pcap_findalldevs: %s\n" % errbuf.value)
        
        self.ui.netcardCb.clear()

        i =0
        d = None
        try:
            d = alldevs.contents
        except:
            QMessageBox.information(None, "提示", "Error in pcap_findalldevs: %s" % errbuf.value)
            QMessageBox.information(None, "提示", "Maybe you need admin privilege?\n")
        while d:
            i = i+1
            self.dNameArr.append(d.name)
            
            desc = ""
            if d.description:
                desc = d.description.decode("utf-8")
            else:
                desc = d.name.decode("utf-8")
            self.dDescriptionArr.append(desc)
            self.ui.netcardCb.addItem(desc)
            
            if d.next:
                d = d.next.contents
            else:
                d = False
        
        pcap_freealldevs(alldevs)

        self.ui.netcardCb.setCurrentIndex(0)
        self.ui.modeCb.setCurrentIndex(0)
    
    def setCallback(self, callback):
        self.callback = callback

    def onClickConfirmBtn(self):
        self.selectedName = self.dNameArr[self.ui.netcardCb.currentIndex()]
        self.selectedMode = self.ui.modeCb.currentIndex()

        if self.callback != None:
            self.callback()
            self.callback = None

        self.close()

    def onClickCancelBtn(self):
        self.close()


class ProtobufTree(QWidget):

    def __init__(self):
        super().__init__()

        self.ui = Ui_ProtobufTree()
        self.ui.setupUi(self)

        flags = Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.initViews()

    def initViews(self):
        clsDic = GenerateData.getProtobufAllMsgs()

        self.ui.treeWidget.clear()
        self.ui.treeWidget.setColumnCount(1)
        
        for k, v in clsDic.items():
            itemPb = QTreeWidgetItem(self.ui.treeWidget)
            itemPb.setText(0, k)
            v.sort(key=lambda x:x.__name__.upper())
            for cls in v:
                itemClass = QTreeWidgetItem(itemPb)
                itemClass.setText(0, cls.__name__)
                for field in cls.DESCRIPTOR.fields:
                    itemField = QTreeWidgetItem(itemClass)
                    itemField.setText(0, field.name)


class MsgIdListUI(QWidget):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MsgIdList()
        self.ui.setupUi(self)

        flags = Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.initViews()

    def initViews(self):
        self.ui.msgIdList.setColumnWidth(0, 50)
        self.ui.msgIdList.setColumnWidth(1, 150)
        self.ui.msgIdList.setColumnWidth(2, 200)
        self.ui.msgIdList.setColumnWidth(3, 180)

        i = 0
        for pData in GenerateData.ProtobufData:
            items = sorted(pData["data"].items(), key=lambda d:d[0], reverse=False)
            for msgId, msgData in items:
                self.ui.msgIdList.insertRow(i)
                item0 = QTableWidgetItem(pData["port"])
                item1 = QTableWidgetItem(str(msgId))
                item2 = QTableWidgetItem(" | ".join(msgData["msgs"]))
                item3 = QTableWidgetItem(msgData["pb"])
                item0.setBackgroundColor(QColor(pData["color"]))
                item1.setBackgroundColor(QColor(pData["color"]))
                item2.setBackgroundColor(QColor(pData["color"]))
                item3.setBackgroundColor(QColor(pData["color"]))
                self.ui.msgIdList.setItem(i, 0, item0)
                self.ui.msgIdList.setItem(i, 1, item1)
                self.ui.msgIdList.setItem(i, 2, item2)
                self.ui.msgIdList.setItem(i, 3, item3)
                i += 1


class FindWin(QWidget):

    def __init__(self):
        super().__init__()

        self.ui = Ui_FindWin()
        self.ui.setupUi(self)

        flags = Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint
        self.setWindowFlags(flags)
        # self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.findCallback = None

        self.initViews()

    def initViews(self):
        self.ui.findBtn.clicked.connect(self.onFindBtn)
        self.ui.cancelBtn.clicked.connect(self.close)
        self.ui.findTxt.returnPressed.connect(self.onFindBtn)

    def onFindBtn(self):
        if self.findCallback != None:
            self.findCallback(self.ui.findTxt.text(), self.ui.upRb.isChecked(), self.ui.upCaseCb.isChecked())

    def setFindCallback(self, findCallback):
        self.findCallback = findCallback

if __name__ == "__main__":

    from PySide2.QtWidgets import QApplication

    app = QApplication(sys.argv)
    win = ControlsPanel()
    win.show()
    sys.exit(app.exec_())