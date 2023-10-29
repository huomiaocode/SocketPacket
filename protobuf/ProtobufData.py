# -*-coding:utf8-*-

class _PacketData:
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

Ack = 0x10
Ack_Push = 0x18


# msgId: { pb, [send, receive] }
ServerData1 = \
{
    "1100": { "pb":"protobuf.pbs.Test_pb2", "msgs":["TestMessage"] },
}

ProtobufData = (
    {
        "ip": "*",
        "port": "443",
        "headlen": "12",
        "endian": "<",
        "color": "#E6D0CE",
        "data": ServerData1
    },
)

def InitServerData():
    pass

def ParsePacketData(index, packetDatas, force:bool):
    packetData:_PacketData = packetDatas[index]
    if not force and packetData.msgIsParsed:
        return packetData.msgStr
    
    packetData.msgStr = "尚未实现"
    packetData.msgIsParsed = True
