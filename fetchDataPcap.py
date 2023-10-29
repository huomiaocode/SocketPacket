# -*-coding:utf8-*-

import os
import socket
import dpkt
import datetime
from PySide2.QtCore import QThread, Signal
from winpcapy import *
from datas import PacketData
import GenerateData

class FetchDataThread(QThread):
    """
    New Thread to fetch raw data
    """

    onPacket = Signal(PacketData)

    def __init__(self, adhandle=None, isWebSocket=False):
        QThread.__init__(self)

        self.processPid = None
        self.adhandle = adhandle
        self.isWebSocket = isWebSocket
        
        self.running = False
        self.tcpDic = {}

    def run(self):
        self.running = True
        
        PHAND = CFUNCTYPE(None, POINTER(c_ubyte), POINTER(pcap_pkthdr), POINTER(c_ubyte))
        packet_handler = PHAND(self._packet_handler)
        pcap_loop(self.adhandle, -1, packet_handler, None)
        pcap_close(self.adhandle)

    def Close(self):
        if self.running:
            self.running = False
            pcap_breakloop(self.adhandle)

    def setProcessPid(self, pid):
        self.processPid = pid

    def _packet_handler(self, param, header, pkt_pointer):
        pkt_data = string_at(pkt_pointer, header.contents.len)
        p = dpkt.ethernet.Ethernet(pkt_data)
        if p.data.__class__.__name__ == 'IP' and p.data.data.__class__.__name__=='TCP':
            self.filterData(p.data)

    def filterData(self, ipPacket):
        srcIp = socket.inet_ntoa(ipPacket.src)
        dstIp = socket.inet_ntoa(ipPacket.dst)
        srcPort = "%s" % ipPacket.data.sport
        dstPort = "%s" % ipPacket.data.dport
        
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
        
        packetData = self.getPacketData(ipPacket, srcIp, srcPort, dstIp, dstPort)
        
        if self.isWebSocket:
            self.parseWebSocketData(packetData)
        else:
            self.parseSocketData(packetData)

    def getPacketData(self, ipPacket, srcIp, srcPort, dstIp, dstPort):
        packetData = PacketData()
        packetData.tcpKey = "%s:%s-%s:%s" % (srcIp, srcPort, dstIp, dstPort)
        packetData.ipPacket = ipPacket

        for pData in GenerateData.ProtobufData:
            pIp = pData["ip"]
            pPort = pData["port"]
            pColor = pData["color"]
            pHeadLen = int(pData["headlen"])
            pEndian = pData["endian"]=="<" and "<" or ">"
            if (srcPort == pPort or dstPort == pPort) and (pIp == "*" or pIp == srcIp):
                packetData.isRecv = srcPort == pPort
                packetData.packetTime = str(datetime.datetime.now().time())[:-3]
                packetData.srcIp = srcIp
                packetData.srcPort = srcPort
                packetData.dstIp = dstIp
                packetData.dstPort = dstPort
                packetData.packetColor = pColor
                packetData.headLen = pHeadLen
                packetData.endian = pEndian
                break
        return packetData

    def parseSocketData(self, packetData:PacketData):
        self.callBackData(packetData)
    
    def parseWebSocketData(self, packetData:PacketData):
        self.callBackData(packetData)
    
    def callBackData(self, packetData:PacketData):
        self.onPacket.emit(packetData)


if __name__ == "__main__":
    pass