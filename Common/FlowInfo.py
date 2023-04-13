# 用来存放flow中会改变的信息，该flow发送的packet个数
class _FlowInfo:
    def __init__(self,pps=0,flowID=0,packetNum=0,realSendNum=0,moniter_pipe=-1):
        self.pps=pps
        self.flowID=flowID
        self.moniter = moniter_pipe
        self.packet_num=packetNum
        self.real_send_num=realSendNum

    def setPacketNumber(self,packetNum):
        self.packet_num = packetNum

    def setRealSendNum(self, realSendNum):
        self.real_send_num=realSendNum

    def setMoniterPipe(self, moniterpipe):
        self.moniter = moniterpipe


