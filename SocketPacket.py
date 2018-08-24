# -*- coding:utf8 -*-

import wx

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
    app = wx.PySimpleApp(redirect=False)
    wx.MessageBox(u"你需要安装pcap类库！")
    sys.exit()

import views
import GenerateData
import myImgs
import re
import os
import pickle
import datetime


class TexaspokerMainWin(wx.Frame):
    """
    数据查看器，主程序
    """

    def __init__(self):
        wx.Frame.__init__(self, None, -1, u"协议数据分析工具", size=(1180, 650))

        self.canParseItemData = True
        self.listAutoScroll = False
        self.listData = []		#(时间，类名，大小，数据，数据类型，是否已经解析)		

        self.SetIcon(myImgs.AppIcon.GetIcon())
        #self.AddStatusBar()
        self.AddViews()

        self.AddMenus()
        self.AddEvents()

    def AddViews(self):
        #左右分割窗
        splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        splitter.SetMinimumPaneSize(430)

        #左边列表
        lPanel = wx.Panel(splitter)
        self.lList = views.DataList(lPanel, self.listData)
        lSizer = wx.BoxSizer(wx.VERTICAL)
        lSizer.Add(self.lList, 1, wx.EXPAND)
        lPanel.SetSizer(lSizer)


        rPanel = wx.Panel(splitter)
        #右上方按钮
        self.rtPanel = views.ControlsPanel(rPanel)
        self.rtPanel.SetDataCallback(self.dataGetted)
        #右下方文本区
        self.rText = wx.TextCtrl(rPanel, -1, style=wx.TE_MULTILINE|wx.TE_RICH|wx.TE_PROCESS_ENTER)
        rSizer = wx.BoxSizer(wx.VERTICAL)
        rSizer.Add(self.rtPanel, 0)
        rSizer.Add(self.rText, 1, wx.EXPAND)
        rPanel.SetSizer(rSizer)

        splitter.SplitVertically(lPanel, rPanel, 660)

        self.dropTarget = views.MFileDropTarget(self)
        self.lList.SetDropTarget(self.dropTarget)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter, 1, wx.EXPAND)

        self.SetSizer(sizer)

    def AddMenus(self):
        self.listPopupMenu = wx.Menu()
        self.listPopupMenu.Append(-1, u"清除所有数据")
        self.listPopupMenu.Append(-1, u"保存所选数据")
        self.listPopupMenu.Append(-1, u"自动滚动列表", kind=wx.ITEM_CHECK)

    def AddEvents(self):
        self.Bind(wx.EVT_CLOSE, self.OnClear)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected, self.lList)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnListContextMenu, self.lList)
        self.Bind(wx.EVT_MENU, self.OnMenuSelected)

        self.lList.Bind(wx.EVT_KEY_DOWN, self.OnKeyEvt)
        self.rText.Bind(wx.EVT_KEY_DOWN, self.OnKeyEvt)
        self.Bind(wx.EVT_FIND, self.OnFind)
        self.Bind(wx.EVT_FIND_NEXT, self.OnFind)
        self.Bind(wx.EVT_FIND_CLOSE, self.OnFindClose)

    def AddStatusBar(self):
        self.sb = self.CreateStatusBar()
        self.sb.SetFieldsCount(1)

    def dataGetted(self, data):
        # 删除多出来的数据
        maxSize = 2000
        delCount = 100
        offsetLen = len(self.listData) - maxSize
        if offsetLen>=0:
            for i in xrange(0, delCount+offsetLen):
                self.listData.pop(0)
            self.lList.SetItemCount(len(self.listData))
            self.lList.Refresh(False)

        #数据处理
        if data[1] == "":
            data[1] = GenerateData.GetProtobufMsgName(data[5], data[4], data[0]==u"接收")
        self.listData.append(data)
        listLen = len(self.listData)
        self.lList.SetItemCount(listLen)
        if(self.listAutoScroll):
            self.lList.ScrollList(0, 30)

        self.lList.RefreshItem(listLen-1)

    def OnKeyEvt(self, event):
        event.Skip()
        needReturn = False
        searchFrom = ""
        searchText = ""
        if event.GetEventObject() == self.lList:
            searchFrom = "list"
        elif event.GetEventObject() == self.rText:
            searchFrom = "text"
            fromPos, toPos = self.rText.GetSelection()
            searchText = self.rText.GetValue()[fromPos:toPos]
        # Ctrl+F
        if searchFrom!="" and event.GetKeyCode()==70 and event.ControlDown():
            if not hasattr(self, "findData"):
                self.findData = wx.FindReplaceData()
            self.findData.SetFindString(searchText)
            if hasattr(self, "dlg"):
                self.dlg.searchObj = {"fromStr":searchFrom}
                self.dlg.SetFocus()
                self.dlg.Show()
                return

            self.dlg = wx.FindReplaceDialog(event.GetEventObject(), self.findData, u"查找", wx.FR_NOUPDOWN)
            self.dlg.searchObj = {"fromStr":searchFrom}
            self.dlg.Show()
        # Ctrl+O
        if searchFrom=="list" and event.GetKeyCode()==79 and event.ControlDown():
            dlg = wx.FileDialog(self, message=u"选择文件...", defaultDir="",defaultFile="",
                                wildcard=u"数据文件(*.pickle)|*.pickle", style=wx.OPEN|wx.MULTIPLE)
            if dlg.ShowModal() == wx.ID_OK:
                self.OpenPickleFiles(*dlg.GetPaths())
            dlg.Destroy()
        # Ctrl+A
        if searchFrom=="list" and event.GetKeyCode()==65 and event.ControlDown():
            self.canParseItemData = False
            count = self.lList.GetItemCount()
            for n in xrange(0, count):
                self.lList.SetItemState(n, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
            self.canParseItemData = True
    def OpenPickleFiles(self, *path):
        dataArr = []
        for i in xrange(len(path)):
            try:
                fp = open(path[i], "rb")
                dataArr.extend(pickle.load(fp))
            except Exception:
                print "something is error !"
            finally:
                fp.close()

        if len(dataArr)>0:
            dataArr.insert(0, ['', 'import start', datetime.datetime.now().time(), 0, '', 0, '', True, '', '', ''])
            dataArr.append(['', 'import end', '', 0, '', 0, '', True, '', '', ''])
            self.listData.extend(dataArr)
            self.lList.SetItemCount(len(self.listData))
            self.lList.Refresh(False)

    def OnFind(self, event):
        findStr = self.findData.GetFindString()
        findFlag = self.findData.GetFlags()
        searchObj = self.dlg.searchObj
        findDown = findFlag & wx.FR_DOWN == wx.FR_DOWN
        findCase = findFlag & wx.FR_MATCHCASE == wx.FR_MATCHCASE
        findWhole = findFlag & wx.FR_WHOLEWORD == wx.FR_WHOLEWORD

        if findWhole:
            if findCase:
                regExp = re.compile(r"\b"+findStr+r"\b")
            else:
                regExp = re.compile(r"\b"+findStr+r"\b", re.IGNORECASE)
        else:
            if findCase:
                regExp = re.compile(findStr)
            else:
                regExp = re.compile(findStr, re.IGNORECASE)

        if searchObj["fromStr"] == "text":
            txtStr = self.rText.GetValue()
            fromPos, toPos = self.rText.GetSelection()
            result = regExp.search(txtStr, toPos)
            if not result:
                result = regExp.search(txtStr)
            if result:
                self.rText.SetSelection(result.start(), result.end())
                self.rText.SetFocus()
        elif searchObj["fromStr"] == "list":
            def findListIndexByStrFunc(listData, listDataLen, regExp, startIndex):
                findIndex = -1
                for index in xrange(startIndex, listDataLen):
                    data = listData[index]
                    if regExp.search(str(data[0])) or\
                       regExp.search(str(data[1])) or\
                       regExp.search(str(data[2])) or\
                       regExp.search(str(data[3])) or\
                       regExp.search(str(data[4])) or\
                       regExp.search(hex(data[5])) or\
                       regExp.search(str(data[10])):
                        findIndex = index
                        break
                return findIndex

            listDataLen = len(self.listData)
            if listDataLen == 0:
                return
            startIndex = self.lList.GetFirstSelected() + 1
            if startIndex>=listDataLen:
                startIndex = 0
            findIndex = findListIndexByStrFunc(self.listData, listDataLen, regExp, startIndex)
            if findIndex == -1:
                findIndex = findListIndexByStrFunc(self.listData, listDataLen, regExp, 0)
            if findIndex != -1:
                selectedIndex = self.lList.GetFirstSelected()
                while selectedIndex!=-1:
                    self.lList.SetItemState(selectedIndex, 0, -1)
                    selectedIndex=self.lList.GetNextSelected(selectedIndex)
                    
                self.lList.Select(findIndex)
                self.lList.EnsureVisible(findIndex)
                self.lList.SetFocus()

    def OnFindClose(self, event):
        self.dlg.Destroy()
        del self.dlg

    def OnListItemSelected(self, event):
        if not self.canParseItemData:
            return
        
        row = event.m_itemIndex
        rowArr= self.listData[row]

        if not rowArr[7]:	#数据未解析
            rowArr[7] = True
            rowArr[8] = GenerateData.GetProtobufMsgData(rowArr[1], rowArr[4], rowArr[6], rowArr[12])

        try:
            tmpValue = u'时间：%s\n类名：%s\n大小：%d\n数据：\n\n%s' % (rowArr[2], rowArr[1], rowArr[3], rowArr[8])
            self.rText.SetValue(tmpValue)
        except Exception, err:
            self.rText.SetValue(repr(rowArr[8]))

    def OnListContextMenu(self, event):
        self.PopupMenu(self.listPopupMenu)

    def OnMenuSelected(self, event):
        evtObj = event.GetEventObject()
        evtMenu = evtObj.FindItemById(event.GetId())
        caption = evtMenu.GetText()
        if(caption == u"清除所有数据"):
            while len(self.listData)>0:
                self.listData.pop()
            self.lList.SetItemCount(0)
        elif(caption == u"自动滚动列表"):
            self.listAutoScroll = evtMenu.IsChecked()
        elif(caption == u"保存所选数据"):
            lastPos = self.lList.GetFirstSelected()
            selectedArr = []
            while lastPos!=-1:
                selectedArr.append(self.listData[lastPos])
                lastPos = self.lList.GetNextSelected(lastPos)
            if len(selectedArr)>0:
                dlg = wx.FileDialog(self, message=u"保存文件至...", defaultDir='', defaultFile="",
                                    wildcard=u"数据文件(*.pickle)|*.pickle", style=wx.SAVE|wx.OVERWRITE_PROMPT)
                if dlg.ShowModal() == wx.ID_OK:
                    path = dlg.GetPath()
                    fp = open(path, "wb")
                    pickle.dump(selectedArr, fp)
                    fp.close()
                dlg.Destroy()

    def OnClear(self, event):
        #self.rtPanel.OnClear(event)
        if event:
            event.Skip()
            sys.exit()

    def Trace(self, data):
        print data


if __name__ == "__main__":
    app = wx.PySimpleApp(redirect=False)
    frame = TexaspokerMainWin()
    frame.Show()
    print "app run!"
    app.MainLoop()