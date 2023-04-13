# ElasticSketch类
'''
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
'''

# sketch基类
import Utility.Hash
import Common.Flow
import Common.FlowInfo


class _Elastic_Sketch:
    def __init__(self, d, ws, active, hashFunction):#, switch_ID
        #self.switch_ID = switch_ID
        # 哈希表长宽
        self.hashfunc = hashFunction
        self.active = active
        self.d = d
        # sketch表的w
        self.sketch_w = ws

        # 工具类
        self.cntq = 0
        self.qlist = []
        self.hash = Utility.Hash._Hash()
        self.heavy_counter = 0
        self.light_counter = 0
        # 哈希表    二维数组
        self.light_table = []
        self.heavy_table = []
        # light的counter的最大值
        self.light_Max = 2**8-1
        # heavy的counter的最大值
        self.heavy_Max = 2**32-1
        # 门限值
        self.threshold = 8
        self.Partation()
        self.Generate_Hash_Table()


    # 生成对应的哈希表并初始化，根据d和w初始化hash_table，为每行固定一种hash方法
    def Generate_Hash_Table(self):
        # 生成lisht
        for i in range(0, self.d):
            self.light_table.append([0 for x in range(0, self.light_counter)])
        # 生成heavy
        for x in range(0, self.heavy_counter):
            self.heavy_table.append([])


    # common模式下收包处理逻辑
    def Receive_packet_common(self, flowID, flowSize):#packet：将原参数packet改为flowID；增加了flowSize参数
        # 处理heavy的部分
        heavy_hash = self.hash.Hash_Function(str(flowID), self.heavy_counter, self.hashfunc[0])
        if self.heavy_table[heavy_hash] == []:
            self.heavy_table[heavy_hash] = [flowID,flowSize,False,0]
        elif self.heavy_table[heavy_hash][0] == flowID:
            self.heavy_table[heavy_hash][1] += flowSize
        elif not self.heavy_table[heavy_hash][0] == flowID:
            self.heavy_table[heavy_hash][3] += flowSize
            if self.heavy_table[heavy_hash][3]/self.heavy_table[heavy_hash][1] < self.threshold:
                self.Deliver_light(flowID,flowSize)
            else:
                self.cntq += 1
                self.qlist.append([flowID,self.heavy_table[heavy_hash][0]])
                self.Deliver_light(self.heavy_table[heavy_hash][0],self.heavy_table[heavy_hash][1])
                self.heavy_table[heavy_hash] = [flowID, flowSize, True, 1]
                
    # 接受light part的包
    def Deliver_light(self, flowID,flowSize):
        for i in range(0, self.d):
            hash = self.hash.Hash_Function(str(flowID), self.light_counter, self.hashfunc[i])
            self.light_table[i][hash] += flowSize
    # 查询一个flow对应的counter
    def Query(self,flowID):
        heavy_hash = self.hash.Hash_Function(str(flowID), self.heavy_counter, self.hashfunc[0])
        if self.heavy_table[heavy_hash] == []:
            return [0,False]
        if self.heavy_table[heavy_hash][0] == flowID:
            if self.heavy_table[heavy_hash][2] == False:
                return [self.heavy_table[heavy_hash][1],True]
            elif self.heavy_table[heavy_hash][2] == True:
                return [self.heavy_table[heavy_hash][1]+self.Query_Light(flowID),True]
        elif not self.heavy_table[heavy_hash][0] == flowID:
            return [self.Query_Light(flowID),False]
    # 查询light part的counter
    def Query_Light(self,flowID):
        result = 255
        for i in range(0, self.d):
            hash = self.hash.Hash_Function(str(flowID), self.light_counter, self.hashfunc[i])
            result = min(self.light_table[i][hash],result)
        return result
    # 查询占有率
    def Occupied_NUM(self):
        counts_light = [0 for x in range(0, self.d)]
        sketch_list = self.light_table
        # 在sketch_table里计数统计非0个数
        for i in range(0, self.sketch_w):
            for j in range(0, self.d):
                if not sketch_list[j][i] == 0:
                    counts_light[j] += 1

        counts_heavy = 0
        sketch_list = self.heavy_table
        # 在sketch_table里计数统计非0个数
        for i in range(0, self.heavy_counter):
                if not sketch_list[i] == 0:
                    counts_heavy += 1

        return (sum(counts_light) / (self.light_counter * self.d) + counts_heavy / self.heavy_counter)/2
    # 划分heavy和light
    def Partation(self):
        # sketch的存储空间，单位bit,light和heavy的空间对半分
        sketch_memery = self.sketch_w * 4 * 8 * 2/2
        # 共有空间/单个heavy空间个
        self.heavy_counter = int(sketch_memery/(97+32*2+1))
        # 每个light的counter占8bit，两行
        self.light_counter = int(sketch_memery/(8*2))
        pass




