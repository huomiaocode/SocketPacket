# -*-coding:utf8-*-

import wx
import wx.lib.buttons as buttons
import socket, thread, time
from fetchDataPcap import *
from ctypes import *
from winpcapy import *
import myImgs
import  wx.lib.scrolledpanel as scrolled
import GenerateData


class ControlsPanel(wx.Panel):
	'''
	这个是程序右上方的按钮和文本框
	'''

	processPid = None

	def __init__(self,parent,id=-1):
		wx.Panel.__init__(self,parent,id)
	
		self.isRunning = False
		self.filterStr = ""
		self.threadE = None
		self.dataCallback = None
		self.processPid = None
		self.adhandle = None
		self.enabledArr = []
		self.inputTxtArr = []
		
		self.CreateTopControls()

	def CreateTopControls(self):
		#协议树
		self.protobufTreeBtn = wx.Button(self, -1, u"协议树", size=(70, -1))
		
		#消息表
		self.msgIdBtn = wx.Button(self, -1, u"消息表", size=(70, -1))
		
		#网卡设置
		self.cardsetBtn = wx.Button(self, -1, u"网卡设置", size=(70, 40))
		
		# 输入框面板
		self.ipPortPanel = scrolled.ScrolledPanel(self, size=(295, 105), style=wx.TAB_TRAVERSAL)
		
		self.enabledArr = []
		self.inputTxtArr = []
		
		pDataLen = len(GenerateData.ProtobufData)
		for i in xrange(pDataLen):
			pData = GenerateData.ProtobufData[i]
			labelTxt = wx.TextCtrl(self.ipPortPanel, -1, pData["name"], size=(60, 22))
			ipTxt = wx.TextCtrl(self.ipPortPanel, -1, pData["ip"], size=(100, 22))
			portTxt = wx.TextCtrl(self.ipPortPanel, -1, pData["port"], size=(50, 22))
			headlenTxt = wx.TextCtrl(self.ipPortPanel, -1, pData["headlen"], size=(25, 22))
			endianTxt = wx.TextCtrl(self.ipPortPanel, -1, pData["endian"], size=(20, 22))
			
			txtTuple = (labelTxt, ipTxt, portTxt, headlenTxt, endianTxt)
			self.inputTxtArr.append(txtTuple)
			self.enabledArr.extend(txtTuple)

		#过滤、启动、暂停 按钮
		self.wsCb = wx.CheckBox(self, -1, u"WS", size=(40, 24))
		self.processBtn = buttons.GenBitmapTextButton(self, -1, myImgs.AppPng.GetBitmap(), u"所有进程", size=(80,24), style=wx.BORDER_NONE)
		self.filterBtn = wx.Button(self, -1, u"过滤", size=(120, -1))
		self.startBtn = wx.Button(self, -1, u"启动", size=(120, 35))

		self.wsCb.SetValue(False)
		self.filterBtn.Disable()
		self.startBtn.Disable()

		# 暂时隐藏
		self.wsCb.Hide()
		
		self.enabledArr.append(self.wsCb)
		self.enabledArr.append(self.filterBtn)
		self.enabledArr.append(self.cardsetBtn)
		self.enabledArr.append(self.processBtn)
		
		self.Bind(wx.EVT_BUTTON, self.OnProtobufTree, self.protobufTreeBtn)
		self.Bind(wx.EVT_BUTTON, self.OnMsgIdList, self.msgIdBtn)
		self.Bind(wx.EVT_BUTTON, self.OnCardSet, self.cardsetBtn)
		self.Bind(wx.EVT_BUTTON, self.OnFilter, self.filterBtn)
		self.Bind(wx.EVT_BUTTON, self.OnStartUp, self.startBtn)
		
		self.processBtn.Bind(wx.EVT_LEFT_DOWN, self.OnStartPickProcess)
		self.processBtn.Bind(wx.EVT_LEFT_UP, self.OnStopPickProcess)
		self.processBtn.Bind(wx.EVT_RIGHT_DOWN, self.OnClearCurrentProcess)		

		sizer = wx.GridBagSizer(3, 3)
		
		sizer.Add(self.protobufTreeBtn, (0,0))
		sizer.Add(self.msgIdBtn, (1,0))
		sizer.Add(self.cardsetBtn, (2,0))
		
		columnLen = 0
		if len(self.inputTxtArr)>0:
			columnLen = len(self.inputTxtArr[0])
		scrollSizer = wx.GridBagSizer(pDataLen, columnLen)
		
		if columnLen > 0:
			for i in xrange(pDataLen):
				for j in xrange(columnLen):
					scrollSizer.Add(self.inputTxtArr[i][j], (i, j))
		
		sizer.Add(self.ipPortPanel, (0, 1), (3, 1))
		
		wsSizer = wx.BoxSizer(wx.HORIZONTAL)
		wsSizer.Add(self.wsCb)
		wsSizer.Add(self.processBtn)

		sizer.Add(wsSizer, (0,2))
		sizer.Add(self.filterBtn, (1,2))
		sizer.Add(self.startBtn, (2,2))
		
		self.ipPortPanel.SetSizer(scrollSizer)
		self.ipPortPanel.SetAutoLayout(1)
		self.ipPortPanel.SetupScrolling()
		self.SetSizer(sizer)

		return sizer
	
	def OnProtobufTree(self, event):
		if not hasattr(self, "protobufTree"):
			self.protobufTree = MProtobufTree()
		
		self.protobufTree.Show()
		self.protobufTree.Restore()
		self.protobufTree.Raise()
		
	def OnMsgIdList(self, event):
		if not hasattr(self, "msgIdList"):
			self.msgIdList = MMsgIdList()
		
		self.msgIdList.Show()
		self.msgIdList.Restore()
		self.msgIdList.Raise()
	
	def OnCardSet(self, event):
		if not hasattr(self, "cardset"):
			self.cardset = CardSetWin(wx.GetActiveWindow())
		
		self.cardset.CenterOnParent()
		
		if wx.ID_OK == self.cardset.ShowModal():
			self.selectedName = self.cardset.selectedName
			self.selectedMode = self.cardset.selectedMode
			self.filterBtn.Enable()

	def GetTextValue(self, txt):
		return txt.GetValue().strip().encode("gbk")
	
	def OnFilter(self, event):
		self.filterStr = ""
		
		for i in xrange(len(self.inputTxtArr)):
			name = self.GetTextValue(self.inputTxtArr[i][0])
			ip = self.GetTextValue(self.inputTxtArr[i][1])
			port = self.GetTextValue(self.inputTxtArr[i][2])
			headlen = self.GetTextValue(self.inputTxtArr[i][3])
			endian = self.GetTextValue(self.inputTxtArr[i][4])
			
			pData = None
			for _pData in GenerateData.ProtobufData:
				if _pData["name"] == name:
					pData = _pData
					break
			
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
			if self.filterStr!="":
				self.filterStr += " or "
			if ipPortStr!="":
				self.filterStr += "(%s)" % ipPortStr
		
		self.startBtn.Enable()

	def OnStartUp(self, event):
		if not self.isRunning:
			adhandle = self.GetHandle()
			if not adhandle:
				wx.MessageBox(u"获取pcap句柄为空！")
				return
			
			self.isRunning = True
			self.threadE = FetchDataThread("getProtobufData", self.dataCallback, adhandle, self.wsCb.IsChecked())
			self.threadE.SetProcessPid(self.processPid)
			self.threadE.start()
			
			self.startBtn.SetLabel(u"暂停")
			for obj in self.enabledArr:
				obj.Disable()
		else:
			self.isRunning = False
			self.threadE.Close()
			self.threadE = None
			
			self.startBtn.SetLabel(u"启动")
			for obj in self.enabledArr:
				obj.Enable()

	def GetHandle(self):
		errbuf= create_string_buffer(PCAP_ERRBUF_SIZE)
		adhandle = pcap_open_live(self.selectedName, 65536, self.selectedMode, 1000, errbuf)				

		fcode = bpf_program()
		if pcap_compile(adhandle,byref(fcode),self.filterStr,1,0) < 0:
			wx.MessageBox(u"编译出错，语法不正确。")
			pcap_close(adhandle)
       
		if pcap_setfilter(adhandle,byref(fcode)) < 0:
			wx.MessageBox(u"设置filter时出错！")
			pcap_close(adhandle)
			
		return adhandle
	
	def OnClearCurrentProcess(self, event):
		event.Skip()
		self.processBtn.SetLabel(u"所有进程")
		self.processBtn.Refresh()
		self.processPid = None
		if self.threadE:
			self.threadE.SetProcessPid(self.processPid)	
	
	def OnStartPickProcess(self, event):
		event.Skip()
		
	def OnStopPickProcess(self, event):
		event.Skip()
		self.OnPickingProcess(None)
		if self.threadE:
			self.threadE.SetProcessPid(self.processPid)

	def OnPickingProcess(self, event):
		try:
			import win32gui, win32process		
			
			cursorPos = win32gui.GetCursorPos()
			hwnd = win32gui.WindowFromPoint(cursorPos)
			pid = repr(win32process.GetWindowThreadProcessId(hwnd)[1])
			self.processBtn.SetLabel(pid)
			self.processBtn.Refresh()
			self.processPid = pid
		except:
			wx.MessageBox (u"你需要安装pywin32模块")
			pass

	def SetDataCallback(self, callback):
		self.dataCallback = callback


class CardSetWin(wx.Dialog):
	"""
	网卡设置界面
	"""

	def __init__(self, parent):
		self.dNameArr = []
		self.dDescriptionArr = []
		self.selectedName = None
		self.selectedMode = 0
		
		pre = wx.PreDialog()
		pre.Create(parent, -1, u"选择网卡及打开模式", size=(350, 150))
		self.PostCreate(pre)		
		
		cardTxt = wx.StaticText(self, -1, u"选择要监视的网卡", pos=(10, 10))
		self.cardComb = wx.Choice(self, -1, pos=(10, 30), size=(325, -1))
		
		modeTxt = wx.StaticText(self, -1, u"选择打开模式", pos=(10, 60))
		self.modeComb = wx.Choice(self, -1, pos=(10, 80), size=(125, -1))
		
		okBtn = wx.Button(self, wx.ID_OK, u"确定", pos=(168, 80), size=(72, -1))
		cancelBtn = wx.Button(self, wx.ID_CANCEL, u"取消", pos=(260, 80), size=(72, -1))
		
		okBtn.SetDefault()
		
		self.Bind(wx.EVT_BUTTON, self.OnOk, okBtn)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, cancelBtn)
		
		errbuf= create_string_buffer(PCAP_ERRBUF_SIZE)
		alldevs=POINTER(pcap_if_t)()
		
		if pcap_findalldevs(byref(alldevs), errbuf) == -1:
			wx.MessageBox("Error in pcap_findalldevs: %s\n" % errbuf.value)
		i=0
		d = None
		try:
			d=alldevs.contents
		except:
			wx.MessageBox ("Error in pcap_findalldevs: %s" % errbuf.value)
			wx.MessageBox ("Maybe you need admin privilege?\n")
		while d:
			i=i+1
			self.dNameArr.append(d.name)
			
			if d.description:
				self.dDescriptionArr.append(d.description)
			else:
				self.dDescriptionArr.append(d.name)
			
			if d.next:
				d=d.next.contents
			else:
				d=False
				
		pcap_freealldevs(alldevs)
		
		self.cardComb.SetItems(self.dDescriptionArr)
		self.modeComb.SetItems([u"直接模式", u"混杂模式"])
		
		self.cardComb.SetSelection(0)
		self.modeComb.SetSelection(0)
		
	def OnOk(self, event):
		self.selectedName = self.dNameArr[self.cardComb.GetSelection()]
		self.selectedMode = self.modeComb.GetSelection()
		
		event.Skip()

	def OnCancel(self, event):
		event.Skip()
	

class DataList(wx.ListCtrl):
	'''
	这是程序左边的列表
	'''
	
	def __init__(self, parent, dataSource):
		wx.ListCtrl.__init__(
			self, parent, -1, 
			style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES
			)
		
		self.dataSource = dataSource
		
		self.InsertColumn(0, u"方向")
		self.InsertColumn(1, u"类型")
		self.InsertColumn(2, u"时间")
		self.InsertColumn(3, u"大小")
		self.InsertColumn(4, u"服务")
		self.InsertColumn(5, u"消息ID")
		self.InsertColumn(6, u"端口")
		self.InsertColumn(7, u"服务器IP")

		self.SetColumnWidth(0, 40)
		self.SetColumnWidth(1, 180)
		self.SetColumnWidth(2, 100)
		self.SetColumnWidth(3, 55)
		self.SetColumnWidth(4, 45)
		self.SetColumnWidth(5, 60)
		self.SetColumnWidth(6, 60)
		self.SetColumnWidth(7, 95)
		
		self.attrDic = {}

	def OnGetItemText(self, item, col):
		dataLen = len(self.dataSource)
		if item>dataLen-1 or dataLen==0:
			return
		if col == 5:
			#return "0x"+hex(self.dataSource[item][col]).upper()[2:]
			return str(self.dataSource[item][col])
		if col == 6:
			return str(self.dataSource[item][10])
		if col == 7:
			return str(self.dataSource[item][11])
		return self.dataSource[item][col]

	def OnGetItemAttr(self, item):
		if item>=len(self.dataSource):
			return None
		
		row = self.dataSource[item]
		
		attr_ = None
		if not hasattr(self.attrDic, "attr_"+row[4]):
			attr_ = wx.ListItemAttr()
			attr_.SetBackgroundColour(row[9])
			self.attrDic["attr_"+row[4]] = attr_
		else:
			attr_ = getattr(self.attrDic, "attr_"+row[4])
		
		if row[0] == u"发送":
			attr_.SetTextColour("#487888")
		else:
			attr_.SetTextColour("#000000")
		
		return attr_


class MFileDropTarget(wx.FileDropTarget):
	def __init__(self, window):
		wx.FileDropTarget.__init__(self)
		self.window = window
	
	def OnDropFiles(self, x, y, filenames):
		self.window.OpenPickleFiles(*filenames)
		

class MProtobufTree(wx.Frame):
	def __init__(self, parent=None):
		wx.Frame.__init__(self, parent, -1, title=u"协议树", size=(400, 450))
		self.SetMinSize((300, 400))
		
		self.tree = wx.TreeCtrl(self, -1)
		self.SetData()
		
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		
	def SetData(self):
		self.root = self.tree.AddRoot(u"根节点")
		self.tree.SetPyData(self.root, None)
		
		clsDic = GenerateData.GetProtobufClass()
		
		for k, v in clsDic.iteritems():
			child = self.tree.AppendItem(self.root, k)
			self.tree.SetPyData(child, None)
			v.sort(key=lambda x:x.__name__.upper())
			for cls in v:
				child2 = self.tree.AppendItem(child, cls.__name__)
				self.tree.SetPyData(child2, None)
				for field in cls.DESCRIPTOR.fields:
					child3 = self.tree.AppendItem(child2, field.name)
					self.tree.SetPyData(child3, None)
		
		self.tree.Expand(self.root)
		
	def OnClose(self, event):
		self.Hide()
		

class MMsgIdList(wx.Frame):
	def __init__(self, parent=None):
		wx.Frame.__init__(self, parent, title=u"消息表", size=(500, 430))
		self.SetMinSize((500, 400))
		
		self.iList = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_VRULES)
		self.iList.InsertColumn(0, u"来源")
		self.iList.InsertColumn(1, u"消息ID")
		self.iList.InsertColumn(2, u"消息名称")
		self.iList.SetColumnWidth(0, 50)
		self.iList.SetColumnWidth(1, 90)
		self.iList.SetColumnWidth(2, 314)
		self.SetData()
		
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		
	def SetData(self):
		i = 0
		for pData in GenerateData.ProtobufData:
			items = sorted(pData["data"].iteritems(), key=lambda d:d[0], reverse=False)
			for k, v in items:
				self.iList.InsertStringItem(i, pData["name"])
				self.iList.SetStringItem(i, 1, "0x"+("00000000"+hex(k).upper()[2:])[-8:])
				self.iList.SetStringItem(i, 2, " | ".join([str(x) for x in v]))
				self.iList.SetItemBackgroundColour(i, pData["color"])
				i += 1
		
	def OnClose(self, event):
		self.Hide()

# test
if __name__ == "__main__":
	pass
