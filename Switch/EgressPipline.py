# egress pipeline类
import Sketch.ElasticSketch
import Switch.SwitchQueue
class _Egress_Pipeline:
    def __init__(self, id, k, w, d=2) -> None:
        self.pipeline_number = k
        self.pipeline_id = id
        self.cnt = 0
        #self.port = []  # 对应的输出端口
        self.w = w
        self.d = d
        self.hashfunc = ["MD5","SHA256"]
        self.main_sketch = Sketch.ElasticSketch._Elastic_Sketch(d=self.d,ws=self.w,active=True,hashFunction=self.hashfunc)
        #self.packet_queue = Switch.Queue._Pipe_Queue(id=id, maxsize=0)
        self.Init_Egress_Pipeline()

    # 初始化egress pipeline的信息以及main sketch和queue
    def Init_Egress_Pipeline(self):
        self.main_sketch.Generate_Hash_Table()
        #if self.packet_queue.empty() != 0:
        #    self.packet_queue.clear()
    
    # 从队列中接收并处理包，读取其中的metadata信息，然后将包发送给出口port
    def Process_Pacekt(self, packet):
        self.cnt += 1
        if packet.metadata != None:
            for ele in packet.metadata.data:
                g_id, g_flowsize= ele
                self.main_sketch.Receive_packet_common(g_id,g_flowsize)
                #print(str(self.pipeline_id)+"pipe接收到流"+str(g_id)+"大小为"+str(g_flowsize)+"的包")
        #else:
        #    self.main_sketch.Receive_packet_common(packet.flow.flowInfo.flowID,1)
    
    # 从队列中接收并处理包，不考虑metadata信息
    def Process_Pacekt_Common(self, packet):
        self.cnt += 1
        self.main_sketch.Receive_packet_common(packet.flow.flowInfo.flowID,1)
    
    def Query(self, flowID):
        return self.main_sketch.Query(flowID)