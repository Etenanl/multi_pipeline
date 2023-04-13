# 包的metadata携带delta sketch信息，实际载荷不做修改

class _Packet:
    def __init__(self):
        self.flow = None
        self.in_pipe = -1
        self.out_pipe = -1
        self.packet_size = 1
        self.metadata = None
    
    # 将流的信息注入到包中,并（随机）指定ingress port和egress port
    # 参数
        # 需要传入的flow对象
        # 输入端口
        # 输出端口
        # 包大小，包计数的话默认为1，bit计数可以修改这个参数
    def New_Packet(self,flow,in_pipe = -1,out_pipe = -1,size = 1):
        self.flow = flow
        self.packet_size = size
        self.in_pipe = in_pipe
        self.out_pipe = out_pipe
        self.metadata = None

    # 将读取到的delta sketch信息写入到包的metadata中
    # 将g_delta传给metadata，如果自己的metadata为空就创建，否则就修改值
    def Modify_metadata(self, g_delta):
        if self.metadata is None:
            self.metadata = _MetaData(g_delta)
        else:
            self.metadata.Set_data(g_delta)

class _MetaData:
    def __init__(self,data):
        self.data = data

    def Set_data(self,data):
        self.data = data