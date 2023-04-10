# CMsketch类
import Utility.Hash

class _CM_Sketch:
    def __init__(self, w, d=2):
        self.w = w
        self.d = d
        self.sketch_table = []
        self.hash = Utility.Hash._Hash()
        self.Init_Hash_Table()

    # 根据w、d初始化hash表，并分配每一行的hash函数
    def Init_Hash_Table(self):
        pass
    
    # 根据包的流信息进行映射
    def Process_Packet(self, packet):
        pass