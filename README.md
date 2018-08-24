# SocketPacket
游戏协议数据抓取解析工具

只要将所有的proto放进去，然后修改ProtobufData.py文件，将消息id和消息名字对应上，就可以在工具里显示出每条消息的详细内容。

### 项目说明
需要安装wxWidget模块
进程id读取用到了pywin32模块
抓包用到了WinPcap，需要预先安装，在_files里面，网络上下载的亦可使用

### 使用说明
生成exe之后，需要将protobuf文件夹复制到exe同目录里
将proto文件放到protobuf/protos/Proto/里面
执行protobuf/gen_protos.py脚本，将proto文件编译成对应的py文件
修改protobuf/ProtobufData.py文件

ProtobufData.py格式参考：

ServerData = \
{
    10001: ["TestMessage"],
}

ProtobufData = (
    {
        "name": "server",
        "ip": "*",
        "port": "443",
        "headlen": "12",
        "endian": "<",
        "color": "#E6D0CE",
        "data": ServerData
    },
)