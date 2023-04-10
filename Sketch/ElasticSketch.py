# ElasticSketch类
import Utility.Hash

class _Elastic_Sketch:
    def __init__(self, h, w, d=2):
        self.heavy_entry_number = h
        self.light_w = w
        self.lighr_d = d
        self.heavy_table = []
        self.light_table = []
        self.Init_Hash_Table()
    
    #根据h、d、w初始化heavy、light部分的hash表，并分配hash函数
    def Init_Hash_Table(self):
        pass

    # 处理携带delta sketch信息的包
    def Process_Packet(self, packet):
        pass