# -*-coding:utf8-*-

class PacketData:
    def __init__(self) -> None:
        self.isRecv = True
        self.packetTime = ""
        self.msgName = ""
        self.msgId = ""
        self.srcIp = ""
        self.srcPort = 0
        self.dstIp = ""
        self.dstPort = 0

        self.tcpKey = None
        self.packetColor = ""
        self.headLen = 12
        self.endian = "<"
        
        self.ipPacket = None
        self.msgIsParsed = False
        self.msgStr = ""
        self.msgParts = None

class DataFormat:
    BYTES = 0
    DEC = 1
    HEX = 2

class AppData:
    def __init__(self) -> None:
        self.dataFormat = DataFormat.BYTES
        self.packetDatas = []


appData = AppData()
