# -*- coding:utf8 -*-

from PySide2.QtWidgets import QWidget, QAction, QFileDialog, QAbstractItemView
from PySide2.QtCore import Qt, QModelIndex, QAbstractTableModel, QItemSelectionModel, QItemSelection
from PySide2.QtGui import QColor, QKeySequence, QFont, QKeyEvent
from winpcapy import *
import pickle
from views_DataListUI import Ui_DataList
from datas import PacketData, DataFormat, appData
import base64
import re
import dpkt
import GenerateData


class DataList(QWidget):
    '''
    这是程序左边的列表
    '''
    def __init__(self):
        super().__init__()

        self.ui = Ui_DataList()
        self.ui.setupUi(self)

        flags = Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint
        self.setWindowFlags(flags)
        
        self.listAutoScroll = True
        self.canParseItemData = True
        self.detailTextCallback = None
        self.forceParsePacketData = False

        self.findWin = None

        self.initViews()
        self.addMenus()
        self.addEvents()
    
    def initViews(self):
        self.setMinimumWidth(750)

        self.model = DataListModel(self)
        self.modelRootIndex = QModelIndex()
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.selectionModel().selectionChanged.connect(self.onListSelectionChanged)
        self.model.init()

    def addMenus(self):
        action1 = QAction("清除所有的数据", self.ui.tableView)
        action2 = QAction("保存所选的数据", self.ui.tableView)
        action3 = QAction("加载保存的数据", self.ui.tableView)
        action4 = QAction("自动滚动列表", self.ui.tableView)
        action4.setCheckable(True)
        action4.setChecked(self.listAutoScroll)
        action1.triggered.connect(self.onMenuClearDatas)
        action2.triggered.connect(self.onMenuSaveSelected)
        action3.triggered.connect(self.onMenuLoadData)
        action4.triggered.connect(self.onMenuAutoScroll)
        action2.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_S))
        action3.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_O))
        self.ui.tableView.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.ui.tableView.addActions([action1, action2, action3, action4])

    def addEvents(self):
        self.ui.tableView.setShortcutEnabled(True)

    def onMenuClearDatas(self):
        self.model.beginResetModel()
        appData.packetDatas.clear()
        self.model.endResetModel()

    def onMenuSaveSelected(self):
        selectedDataArr = []
        selectedIndexes = self.getSelectedIndexes()
        for selectedIndex in selectedIndexes:
            selectedDataArr.append(appData.packetDatas[selectedIndex.row()])

        if len(selectedDataArr) > 0:
            rets = QFileDialog.getSaveFileName(None, "保存文件至...", "", "数据文件(*.pickle)|*.pickle")
            if rets != None and len(rets) >= 1 and rets[0] != "":
                fp = open(rets[0], "wb")
                pickle.dump(selectedDataArr, fp)
                fp.close()

    def onMenuLoadData(self):
        rets = QFileDialog.getOpenFileName(None, "选择文件...", "", "数据文件(*.pickle)|*.pickle")
        if rets != None and len(rets) >= 1 and rets[0] != "":
            try:
                fp = open(rets[0], "rb")
                self.model.beginResetModel()
                appData.packetDatas.extend(pickle.load(fp))
                self.model.endResetModel()
            except Exception:
                print("something is error !")
            finally:
                fp.close()

    def onMenuAutoScroll(self, checked):
        self.listAutoScroll = checked

    def setDetailTextCallback(self, callback):
        self.detailTextCallback = callback

    def getSelectedIndexes(self, withSort=True):
        selectedIndexes = [ index for index in self.ui.tableView.selectedIndexes() if index.column() == 0 ]
        if withSort:
            selectedIndexes.sort(key = lambda x: x.row())
        return selectedIndexes

    def onListSelectionChanged(self):
        if not self.canParseItemData:
            return

        selectedIndexes = self.getSelectedIndexes()
        selectCount = len(selectedIndexes)
        if selectCount == 0:
            return

        txt = ""
        buff = b""
        msgStr = ""
        msgIndex = 0

        for i in range(selectCount):
            selectedIndex = selectedIndexes[i]
            row = selectedIndex.row()
            packetData:PacketData = appData.packetDatas[row]

            # 如果只选中某个Message的所有Part，则显示这个Message的数据
            if i == 0 and packetData.msgParts != None and packetData.msgParts[0] == 1:
                isRecv = packetData.isRecv
                msgName = packetData.msgName
                msgPartPos = 1
                for j in range(1, selectCount):
                    packetDataJ:PacketData = appData.packetDatas[selectedIndexes[j].row()]
                    if packetDataJ.isRecv == isRecv and packetDataJ.msgName == msgName and packetDataJ.msgParts != None and packetDataJ.msgParts[0] == msgPartPos+1:
                        msgPartPos += 1
                    else:
                        break
                    if j == selectCount-1 and msgPartPos == packetData.msgParts[1]:
                        msgIndex = selectCount-1

            if i == msgIndex:
                msgStr = GenerateData.ParsePacketData(row, appData.packetDatas, self.forceParsePacketData)
                columnCount = self.model.columnCount(None)
                for column in range(0, columnCount):
                    columnHeader = self.model.headerData(column, Qt.Horizontal, Qt.DisplayRole)
                    columnData = self.model.data(self.model.index(row, column), Qt.DisplayRole)
                    txt += f"{columnHeader}: {columnData}\n"
            else:
                if self.forceParsePacketData:
                    GenerateData.ParsePacketData(row, appData.packetDatas, self.forceParsePacketData)

            if packetData.ipPacket != None:
                buff += packetData.ipPacket.data.data

        buffStr = ""
        if appData.dataFormat == DataFormat.BYTES:
            buffStr = str(buff)
        elif appData.dataFormat == DataFormat.DEC:
            buffStr = " ".join([str(x) for x in buff])
        elif appData.dataFormat == DataFormat.HEX:
            buffStr = " ".join([f'{x:02X}' for x in buff])

        txt += f"\n数据: \n{buffStr}"
        txt += f"\n\nBase64: \n{base64.b64encode(buff).decode('utf-8')}"

        if msgStr != "":
            txt += f"\n\n{msgStr}"

        if self.detailTextCallback != None:
            self.detailTextCallback(txt)

    def onDataFormatChanged(self):
        self.onListSelectionChanged()

    def onReParseBuff(self):
        old = self.forceParsePacketData
        self.forceParsePacketData = True
        self.onListSelectionChanged()
        self.forceParsePacketData = old

        selectedIndexes = self.getSelectedIndexes()
        self.model.dataChanged.emit(selectedIndexes[0], selectedIndexes[-1])

    def onData(self, packetData: PacketData):
        maxSize = 20000
        # 删除多出来的数据
        dataLen = len(appData.packetDatas)
        offsetLen = dataLen - maxSize + 1
        if offsetLen >= 0:
            self.model.beginRemoveRows(self.modelRootIndex, 0, offsetLen-1)
            for i in range(0, offsetLen):
                appData.packetDatas.pop(0)
                self.model.removeRow(0)
            self.model.endRemoveRows()
        
        # 添加新数据
        dataLen = len(appData.packetDatas)
        self.model.beginInsertRows(self.modelRootIndex, dataLen, dataLen)
        appData.packetDatas.append(packetData)
        try:
            GenerateData.ParsePacketData(dataLen, appData.packetDatas, True)
        except:
            pass
        self.model.endInsertRows()

        if self.listAutoScroll:
            self.ui.tableView.scrollToBottom()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_F and event.modifiers() == Qt.ControlModifier:
            if self.findWin == None:
                import views
                self.findWin = views.FindWin()
                self.findWin.setFindCallback(self.onFind)
                def onDestroyed():
                    self.findWin = None
                self.findWin.destroyed.connect(onDestroyed)
            self.findWin.show()
            self.findWin.raise_()
        return super().keyPressEvent(event)

    def onFind(self, findStr:str, findBack:bool, matchCase:bool):
        if findStr == "":
            return
        
        regExp = matchCase and re.compile(findStr) or re.compile(findStr, re.IGNORECASE)
        findIndex = -1
        findIndexCurrent = 0

        selectedIndexes = self.getSelectedIndexes()
        if len(selectedIndexes) > 0:
            if not findBack:
                findIndexCurrent = selectedIndexes[-1].row() + 1
            else:
                findIndexCurrent = selectedIndexes[0].row() - 1

        for _ in range(len(appData.packetDatas)):
            findIndexCurrent = findIndexCurrent % len(appData.packetDatas)
            packetData:PacketData = appData.packetDatas[findIndexCurrent]
            if regExp.search(packetData.packetTime) or\
               regExp.search(packetData.msgName) or\
               regExp.search(packetData.msgId) or\
               regExp.search(packetData.tcpKey):
                findIndex = findIndexCurrent
                break
            findIndexCurrent += findBack and -1 or 1

        if findIndex != -1:
            selectionModel = self.ui.tableView.selectionModel()
            indexStart = self.model.index(findIndex, 0)
            indexEnd = self.model.index(findIndex, self.model.columnCount(None)-1)
            selection = QItemSelection(indexStart, indexEnd)
            selectionModel.clear()
            selectionModel.select(selection, QItemSelectionModel.Select)
            self.ui.tableView.scrollTo(indexStart, QAbstractItemView.EnsureVisible)

class DataListModel(QAbstractTableModel):

    def __init__(self, dataList:DataList):
        super().__init__()

        self.dataList = dataList

        self.fontItalic = QFont()
        self.fontItalic.setItalic(True)

        self.headers = [
            ("方向", 40),
            ("时间", 100),
            ("大小", 45),
            ("消息名", 180),
            ("消息ID", 60),
            ("本地端口", 60),
            ("远程IP", 95),
            ("远程端口", 60),
            ("标记", 80),
        ]
        self.packetFlagsKeys = (
            dpkt.tcp.TH_FIN,
            dpkt.tcp.TH_SYN,
            dpkt.tcp.TH_RST,
            dpkt.tcp.TH_PUSH,
            dpkt.tcp.TH_ACK,
            dpkt.tcp.TH_URG,
            dpkt.tcp.TH_ECE,
            dpkt.tcp.TH_CWR,
        )
        self.packetFlagsValues = (
            "FIN",
            "SYN",
            "RST",
            "PUSH",
            "ACK",
            "URG",
            "ECE",
            "CWR",
        )

    def init(self):
        header = self.dataList.ui.tableView.horizontalHeader()
        for i in range(len(self.headers)):
            header.resizeSection(i, self.headers[i][1])

    def getFlagsStr(self, flags):
        if flags in self.packetFlagsKeys:
            return self.packetFlagsValues[self.packetFlagsKeys.index(flags)]
        else:
            rets = []
            for i in range(len(self.packetFlagsKeys)):
                if flags & self.packetFlagsKeys[i] == self.packetFlagsKeys[i]:
                    rets.append(self.packetFlagsValues[i])
            return ",".join(rets)
    
    def headerData(self, section: int, orientation, role: int = ...):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.headers[section][0]
    
    def rowCount(self, parent: QModelIndex):
        return len(appData.packetDatas)

    def columnCount(self, parent: QModelIndex):
        return len(self.headers)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.TextAlignmentRole:
            head = self.headers[index.column()][0]
            if head == "消息名":
                return Qt.AlignLeft
            return Qt.AlignCenter
        elif role == Qt.FontRole:
            data: PacketData = appData.packetDatas[index.row()]
            if data.msgParts != None and data.msgParts[0] < data.msgParts[1]:
                head = self.headers[index.column()][0]
                if head == "消息名":
                    return self.fontItalic
        elif role == Qt.TextColorRole:
            data: PacketData = appData.packetDatas[index.row()]
            return data.isRecv and QColor("#000000") or QColor("#487888")
        elif role == Qt.BackgroundColorRole:
            data: PacketData = appData.packetDatas[index.row()]
            if data.packetColor != "":
                return QColor(data.packetColor)
        elif role == Qt.DisplayRole:
            data: PacketData = appData.packetDatas[index.row()]
            head = self.headers[index.column()][0]
            if head == "方向":
                return "接收" if data.isRecv else "发送"
            elif head == "时间":
                return data.packetTime
            elif head == "大小":
                if data.ipPacket != None:
                    return str(len(data.ipPacket.data.data))
                else:
                    return ""
            elif head == "消息名":
                return data.msgName
            elif head == "消息ID":
                return data.msgId
            elif head == "本地端口":
                return data.dstPort if data.isRecv else data.srcPort
            elif head == "远程IP":
                return data.srcIp if data.isRecv else data.dstIp
            elif head == "远程端口":
                return data.srcPort if data.isRecv else data.dstPort
            elif head == "标记":
                if data.ipPacket != None:
                    return self.getFlagsStr(data.ipPacket.data.flags)

        return None

