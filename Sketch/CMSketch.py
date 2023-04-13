# CMsketch类
import Utility.Hash

class _CM_Sketch:
    def __init__(self, w, active, hashFunction, x=4, d=2):
        self.w = w
        self.d = d
        self.x = x # counter的位数
        self.hashfunc = hashFunction
        self.active = active
        self.sketch_table = []
        self.hash = Utility.Hash._Hash()
        self.Generate_Hash_Table()

    # 生成对应的哈希表并初始化，根据d和w初始化hash_table，为每行固定一种hash方法
    def Generate_Hash_Table(self):
        for i in range (0,self.d):
            self.sketch_table.append( [0 for x in range(0, self.w)])

    # common模式下收包处理逻辑
    def Receive_packet(self,packet):
        # 对每一行进行hash
        for i in range(0,self.d):
            hash = self.hash.Hash_Function(str(packet.flow.flowInfo.flowID),self.w,self.hashfunc[i])
            temp = self.sketch_table[i][hash] + packet.packet_size
            if temp > 2 ** self.x - 1:
                self.sketch_table[i][hash] = 2 ** self.x - 1
            else:
                self.sketch_table[i][hash] = temp

    # 查询一个flow对应的counter并清零
    def Query(self,flowID):
        result = 2 ** self.x - 1
        for i in range(0, self.d):
            hash = self.hash.Hash_Function(str(flowID), self.w, self.hashfunc[i])
            result = min(self.sketch_table[i][hash],result)
            self.sketch_table[i][hash] = 0
        return result
    