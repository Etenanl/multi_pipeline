# 流的类，属性包括流的基本信息，进出端口等
import Common.FlowID
import Common.FlowInfo

class _Flow:
    def __init__(self,pps,flowID):
        # flowid这里用不到，如果想记录五元组可以丢进去
        self.flowid = Common.FlowID._FlowID()
        # flowid，pps的信息纯放在这里。
        # packetNum和realSendNum本来是记录该流发包测量值与真实值，如果你用别的方式记录发包数和测量值可以把这两个变量删掉
        self.flowInfo = Common.FlowInfo._FlowInfo(flowID=flowID,pps=pps)

