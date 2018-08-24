# -*- coding:utf8 -*-

from google.protobuf.internal.containers import *
from google.protobuf import reflection

import sys
import wx
import os
import importlib

protobufModules = {}
GameData = {}
ProtobufData = ()

def loadProtobufs():
	protobufDir = "protobuf"
	pbDir = "pbs"
	pbPath = protobufDir+"/"+pbDir
	
	pDataPath = protobufDir+"/ProtobufData.py"
	if os.path.exists(pDataPath):
		try:
			execfile(pDataPath, globals())
		except:
			app = wx.PySimpleApp(redirect=False)
			wx.MessageBox(u"ProtobufData.py文件解析失败，请检查语法！", u"提示")
			sys.exit()

	# 将程序运行路径放入路径搜索里，方式协议导入失败
	dirname, _ = os.path.split(os.path.abspath(sys.argv[0]))
	sys.path.append(dirname)
	
	if os.path.exists(pbPath):
		names = list(os.listdir(pbPath))
		for fileName in names:
			if fileName.endswith(".py"):
				moduleName = "%s.%s.%s" % (protobufDir, pbDir, fileName[:-3])
				try:
					protobufModules[moduleName] = importlib.import_module(moduleName)
				except:
					app = wx.PySimpleApp(redirect=False)
					wx.MessageBox(u"%s导入失败" % fileName[:-3], u"提示")
					sys.exit()

def  GetProtobufMsgName(msgId, packetType, isSource):
	if type(msgId) == int:
		intId = msgId
	else:
		intId = int(msgId)
	
	msgName = None
	
	for pData in ProtobufData:
		if pData["name"] == packetType and pData["data"].has_key(intId):
			tmp = pData["data"][intId]
			if len(tmp)==1:
				msgName = tmp[0]
			else:
				msgName = tmp[isSource and 1 or 0]
	
	return msgName


def GetProtobufMsgData(msgName, msgType, buff, msgObj):
	if msgName == None:
		return "None"
	
	backStr = ""
	if not msgObj:
		obj = GetClassInstanceByProtoClassName(msgName)
		if obj == None:
			return "Class Not Found"
		try:
			obj.ParseFromString(buff)
			msgObj = obj
		except Exception, err:
			backStr = "%s\n\nError\n\n%s\n\n%s" % (msgName, repr(err), repr(buff))
	
	if backStr == "":
		backStr = msgName + "\n" +  GetProtobufObjStr(msgType, msgObj)
	
	try:
		return backStr.decode("gbk")
	except:
		return backStr


def GetProtobufObjStr(msgType, obj, objStr="", indent=0):
	if hasattr(obj, "DESCRIPTOR"):
		fields = obj.ListFields()
		_objStr = objStr
		for (descrip, fieldValue) in fields:
			objStr += '\n%s%s = %s' % (' '*indent, descrip.name, GetProtobufObjStr(msgType, fieldValue, _objStr, indent+4))
	elif type(obj)==RepeatedCompositeFieldContainer:
		_objStr = objStr
		objStr += "\n%s[" % (' '*indent)
		for obj2 in obj:
			objStr += "\n%s%s" % (' '*(2+indent), obj2.DESCRIPTOR.name)
			objStr += GetProtobufObjStr(msgType, obj2, _objStr, indent+4)
		objStr += "\n%s]" % (' '*indent)
	elif type(obj)==RepeatedScalarFieldContainer:
		_objStr = objStr
		objStr += "["
		i = 0
		for obj2 in obj:
			if i>0:
				objStr += ", "
			i += 1
			objStr += "%s" % GetProtobufObjStr(msgType, obj2, _objStr, indent+4)
		objStr += "]"
	else:
		if isinstance(obj, unicode):
			try:
				return obj.encode('gbk')
			except:
				return obj.encode('utf8')
		elif isinstance(obj, long) or isinstance(obj, int):
			return obj
		else:
			if msgType == "jss":
				try:
					return obj.decode('utf8').encode('gbk')
				except:
					return repr(obj)
			else:
				try:
					obj.decode('gbk')
					return obj
				except:
					return repr(obj)
	
	if isinstance(objStr, unicode):	
		return objStr.encode('gbk')
	else:
		return objStr

def GetClassInstanceByProtoClassName(className):
	for moduleName in protobufModules.keys():
		if moduleName.endswith("__init__"):
			continue
		moduleValue = protobufModules[moduleName]
		keys = getattr(moduleValue.DESCRIPTOR, "message_types_by_name").keys()
		for k in keys:
			if k == className:
				v = getattr(moduleValue, k)
				return v()
	return None


def GetProtobufClass():
	cls = {}
	for moduleName in protobufModules.keys():
		if moduleName.endswith("__init__"):
			continue
		moduleValue = protobufModules[moduleName]
		keys = getattr(moduleValue.DESCRIPTOR, "message_types_by_name").keys()
		for k in keys:
			if not cls.has_key(moduleName):
				cls[moduleName] = []
			cls[moduleName].append(getattr(moduleValue, k))
	return cls
	


loadProtobufs()

