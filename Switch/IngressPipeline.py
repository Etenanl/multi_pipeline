# our solution中的ingress pipeline类
from struct import pack
import Sketch.CMSketch
from Switch.EgressPipline import _Egress_Pipeline
import Utility.Hash
import queue

class _Ingress_Pipeline:
    def __init__(self, k, w, id, d, port_cnt) -> None:
        self.pipeline_number = k
        self.pipeline_id = id
        self.port_per_pipe = port_cnt
        # self.port = [self.id*self.port_per_pipe+i for i in range(0,self.port_per_pipe)]  # 对应的输入端口
        
        self.hashfunc = ["MD5","SHA256"]
        self.pipeline_table = []
        self.hash = Utility.Hash._Hash()
        self.delta_sketch = Sketch.CMSketch._CM_Sketch(w=w,active=True,hashFunction=self.hashfunc,x=4,d=d)
        self.Init_Ingress_Pipeline()

    # 初始化ingress pipeline的信息以及pipeline table和delta sketch
    def Init_Ingress_Pipeline(self):
        #初始化pipeline_table
        for i in range(0,self.pipeline_number):
            self.pipeline_table.append([-1,-1])
        self.delta_sketch.Generate_Hash_Table()

    
    # 处理接收的包并发送给cross bar
    def Process_Pacekt(self, packet):
        # pipeline table可能需要换个hash函数
        moniter_pipeline = self.hash.Hash_Function(str(packet.flow.flowInfo.flowID),self.pipeline_number,"SHA1")
        # 更新pipeline table
        if packet.flow.flowInfo.moniter == -1:
            packet.flow.flowInfo.setMoniterPipe(moniter_pipeline)
        elif packet.flow.flowInfo.moniter != moniter_pipeline:
            print("error")
        moniter_pipeline = packet.flow.flowInfo.moniter
        self.pipeline_table[moniter_pipeline] = [moniter_pipeline, packet.flow.flowInfo.flowID]
        # 随机产生出口流水线（或者出端口）
        # egress_pipeline = random.randint(0, self.pipeline_number-1)
        egress_pipeline = packet.out_pipe
        g_id = -1
        for ele in self.pipeline_table:
            if ele[0] == egress_pipeline:
                # 查找pipeline table，得到g的flow ID
                g_id = ele[1]
        self.delta_sketch.Receive_packet(packet)
        if g_id != -1:
            # 携带g delta信息
            g_delta = self.delta_sketch.Query(g_id)
            if g_delta != 0:
                packet.Modify_metadata([[g_id, g_delta]])
        return packet

class _Packet_Cache_Ingress_Pipeline:
    def __init__(self, k, id, port_cnt, max_length=0):
        self.pipeline_number = k
        self.pipeline_id = id
        self.port_per_pipe = port_cnt
        self.cnt = 0
        #self.port = []  # 对应的输入端口
        self.pipeline_table = [] #pipeline table设置的意义？
        self.hash = Utility.Hash._Hash()
        self.pipe_queue = [queue.Queue(maxsize=max_length) for i in range(0,self.pipeline_number)]
        self.Init_Ingress_Pipeline()
    
    # 初始化ingress pipeline的信息以及pipeline table
    def Init_Ingress_Pipeline(self):
        #初始化pipeline_table
        for i in range(0,self.pipeline_number):
            self.pipeline_table.append([-1,-1])
        for i in range(0,self.pipeline_number):
            if not self.pipe_queue[i].empty():
                self.pipe_queue[i].clear()

    def Process_Pacekt(self, packet):
        self.cnt += 1
        # pipeline table可能需要换个hash函数
        #moniter_pipeline = random.randint(0,self.pipeline_number)
        moniter_pipeline = self.hash.Hash_Function(str(packet.flow.flowInfo.flowID),self.pipeline_number,"SHA1")
        # 更新pipeline table
        if packet.flow.flowInfo.moniter == -1:
            packet.flow.flowInfo.setMoniterPipe(moniter_pipeline)
        elif packet.flow.flowInfo.moniter != moniter_pipeline:
            print("error")
        moniter_pipeline = packet.flow.flowInfo.moniter
        self.pipeline_table[moniter_pipeline] = [moniter_pipeline, packet.flow.flowInfo.flowID]
        # 随机产生出口流水线（或者出端口）
        #egress_pipeline = random.randint(0, self.pipeline_number-1)
        egress_pipeline = packet.out_pipe
        #egress_pipeline= moniter_pipeline
        piggyback_list = []
        if moniter_pipeline != egress_pipeline:
            if not self.pipe_queue[moniter_pipeline].full():
                self.pipe_queue[moniter_pipeline].put(packet.flow.flowInfo.flowID)
                #print(str(packet.flow.flowInfo.flowID)+"流的包放入队列"+str(moniter_pipeline))
        else:
            piggyback_list.append([packet.flow.flowInfo.flowID, 1])
        while not self.pipe_queue[egress_pipeline].empty():
            g_id = self.pipe_queue[egress_pipeline].get()
            piggyback_list.append([g_id,1])
            #print(str(g_id)+"流的包被流"+str(packet.flow.flowInfo.flowID)+"的包带到pipe"+str(egress_pipeline))
        if len(piggyback_list) != 0:
            packet.Modify_metadata(piggyback_list)
        return packet
