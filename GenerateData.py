# -*- coding:utf8 -*-

# 这一行不能删，否者google的库不会被打进包里面
from google.protobuf import descriptor

from PySide2.QtWidgets import QApplication, QMessageBox

import sys
import os
import importlib

ProtobufModules = {}
ProtobufData = ()
def InitServerData():
    pass
def ParsePacketData(index, packetDatas, force):
    pass


def loadProtobufs():
    protobufDir = "protobuf"
    pbDir = "pbs"
    pbPath = protobufDir + "/" + pbDir
    
    pDataPath = protobufDir + "/ProtobufData.py"
    if os.path.exists(pDataPath):
        try:
            with open(pDataPath, "r", encoding="utf-8") as f:
                exec(f.read(), globals())
        except Exception as ex:
            QApplication(sys.argv)
            QMessageBox.information(None, "提示", "ProtobufData.py导入失败 %s" % str(ex))
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
                    ProtobufModules[moduleName] = importlib.import_module(moduleName)
                except Exception as ex:
                    QApplication(sys.argv)
                    QMessageBox.information(None, "提示", "%s导入失败 %s" % (fileName[:-3], str(ex)))
                    sys.exit()

    InitServerData()

def getProtobufAllMsgs():
    cls = {}
    for moduleName in ProtobufModules.keys():
        if moduleName.endswith("__init__"):
            continue
        moduleValue = ProtobufModules[moduleName]
        keys = getattr(moduleValue.DESCRIPTOR, "message_types_by_name").keys()
        for k in keys:
            if moduleName not in cls:
                cls[moduleName] = []
            cls[moduleName].append(getattr(moduleValue, k))
    return cls


loadProtobufs()
