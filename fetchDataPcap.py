# -*-coding:utf8-*-

import os
import threading
import socket
import struct
import dpkt
import datetime
from winpcapy import *
import GenerateData

class FetchDataThread(threading.Thread):
	"""
	New Thread to fetch raw data
	"""

	def __init__(self, threadName, callback=None, adhandle=None, isWebSocket=False):
		threading.Thread.__init__(self, name=threadName)

		self.processPid = None
		self.callback = callback
		self.adhandle = adhandle
		self.isWebSocket = isWebSocket
		
		self.running = False
		self.tcpDic = {}
		
		self.setDaemon(True)

	def run(self):
		self.running = True
		
		PHAND=CFUNCTYPE(None,POINTER(c_ubyte),POINTER(pcap_pkthdr),POINTER(c_ubyte))
		packet_handler=PHAND(self._packet_handler)
		pcap_loop(self.adhandle, -1, packet_handler, None)
		pcap_close(self.adhandle)

	def Close(self):
		if self.running:
			self.running = False
			pcap_breakloop(self.adhandle)

	def SetProcessPid(self, pid):
		self.processPid = pid
		
	def _packet_handler(self, param,header,pkt_data):
		buf = ''
		i = 0
		while i<header.contents.len:
			buf += chr(pkt_data[i])
			i += 1
		
		p = dpkt.ethernet.Ethernet(buf)
		if p.data.__class__.__name__ == 'IP' and p.data.data.__class__.__name__=='TCP':
			self.FilterData(p.data)
	
	def FilterData(self, ipPacket):
		srcIp = socket.inet_ntoa(ipPacket.src)
		dstIp = socket.inet_ntoa(ipPacket.dst)
		srcPort = "%s" % ipPacket.data.sport
		dstPort = "%s" % ipPacket.data.dport
		tcpKey = "%s:%s-%s:%s" % (srcIp, srcPort, dstIp, dstPort)
		
		if self.processPid:
			findIt = False
			net_info = os.popen('netstat -no').readlines()
			srcIpPort = "%s:%s" % (srcIp, srcPort)
			destIpPort = "%s:%s" % (dstIp, dstPort)
			for line in net_info[4:]:
				s = line.split()
				if len(s)>4 and s[4]==str(self.processPid):
					if (srcIpPort==s[2] and destIpPort==s[1]) or (srcIpPort==s[1] and destIpPort==s[2]):
						findIt = True
						break
			if not findIt: return
		
		protoDataInfo = self.GetProtobufDataInfo(srcIp, srcPort, dstIp, dstPort)
		
		if self.isWebSocket:
			self.ParseWebSocketData(ipPacket=ipPacket, tcpKey=tcpKey, protoDataInfo=protoDataInfo)
		else:
			self.ParseSocketData(ipPacket=ipPacket, tcpKey=tcpKey, protoDataInfo=protoDataInfo)

	def GetProtobufDataInfo(self, srcIp, srcPort, dstIp, dstPort):
		protoDataInfo = {
			"isSource": False,
			"clientPort": None,
			"packetType": None,
			"packetColor": None,
			"headLen": 12,
			"endian": "<",
			"protoData": None,
		}

		for pData in GenerateData.ProtobufData:
			pName = pData["name"]
			pIp = pData["ip"]
			pPort = pData["port"]
			pColor = pData["color"]
			pHeadLen = int(pData["headlen"])
			pEndian = pData["endian"]=="<" and "<" or ">"
			if (srcPort == pPort or dstPort == pPort) and (pIp == "*" or pIp == srcIp):
				protoDataInfo["packetType"] = pName
				protoDataInfo["packetColor"] = pColor
				protoDataInfo["headLen"] = pHeadLen
				protoDataInfo["endian"] = pEndian
				protoDataInfo["isSource"] = srcPort == pPort
				protoDataInfo["clientPort"] = dstPort if protoDataInfo["isSource"] else srcPort
				protoDataInfo["serverIp"] = srcIp if protoDataInfo["isSource"] else dstIp
				protoDataInfo["protoData"] = pData["data"]
				break
		return protoDataInfo

	def ParseSocketData(self, ipPacket=None, tcpKey="", protoDataInfo=None):
		# 数据的标记
		flagTuple = (
		        ipPacket.data.flags&dpkt.tcp.TH_FIN,
		        ipPacket.data.flags&dpkt.tcp.TH_SYN,
		        ipPacket.data.flags&dpkt.tcp.TH_RST,
		        ipPacket.data.flags&dpkt.tcp.TH_PUSH,
		        ipPacket.data.flags&dpkt.tcp.TH_ACK,
		        ipPacket.data.flags&dpkt.tcp.TH_URG
		)
		
		# 是否要重置数据
		resetData = flagTuple[0] == 1

		if resetData and self.tcpDic.has_key(tcpKey):
			del self.tcpDic[tcpKey]
		
		if not self.tcpDic.has_key(tcpKey):
			self.tcpDic[tcpKey] = ipPacket.data.data
		else:
			self.tcpDic[tcpKey] += ipPacket.data.data
		
		buff = self.tcpDic[tcpKey]
		buffLen = len(buff)
		
		if protoDataInfo["packetType"] is None:
			return
		
		while buffLen>=8:
			msgType = struct.unpack('%si' % protoDataInfo["endian"], buff[0:4])[0]
			msgLen = struct.unpack('%si' % protoDataInfo["endian"], buff[4:8])[0]
			msgAllLen = msgLen + protoDataInfo["headLen"]
			
			if not self.running:
				break
			
			if buffLen >= msgAllLen:
				#截断数据
				msgStr = buff[protoDataInfo["headLen"]:msgAllLen]
				self.tcpDic[tcpKey] = buff[msgAllLen:]
					
				buff = self.tcpDic[tcpKey]
				buffLen = len(buff)
				
				self.CallBackData(
					protoDataInfo["isSource"],
					protoDataInfo["packetType"],
					msgLen, msgType, msgStr, "", None,
					protoDataInfo["packetColor"],
					protoDataInfo["clientPort"],
					protoDataInfo["serverIp"]
				)
			else:
				break
	
	
	def ParseWebSocketData(self, ipPacket=None, tcpKey="", protoDataInfo=None):
		data = self.GetWebSocketFrameData(ipPacket=ipPacket, tcpKey=tcpKey)
		if data == None:
			return

		dataLen = len(data)
		msgLen = dataLen
		msgId = 0
		msgName = ""
		msg = None

		self.CallBackData(
			protoDataInfo["isSource"],
			protoDataInfo["packetType"],
			msgLen, msgId, "", msgName, msg,
			protoDataInfo["packetColor"],
			protoDataInfo["clientPort"],
			protoDataInfo["serverIp"]
		)

	def GetWebSocketFrameData(self, ipPacket=None, tcpKey=""):
		data = ipPacket.data.data

		# print repr(data)
		return data
	
	def CallBackData(self, isSource, packetType, msgLen, msgType, msgStr, msgName, msg, packetColor, clientPort, serverIp):
		result = \
		[
				isSource and u"接收" or u"发送",			#0
				msgName,									#1、消息对应的类名称
				str(datetime.datetime.now().time())[:-3],	#2
				msgLen,								#3
				packetType,							#4
				msgType,							#5
				msgStr,								#6
				False,								#7、消息是否已经解析过
				"",									#8、消息解码后的数据
				packetColor,						#9、消息在列表里显示的颜色
				clientPort,							#10、客户端的端口
				serverIp,							#11、服务器的IP
				msg,								#12、消息体
		]
		if self.callback:
			self.callback(result)
		else:
			print result


if __name__ == "__main__":
	pass