import Switch.IngressPipeline
import Switch.Crossbar
import queue
import Switch.SwitchQueue
import Switch.EgressPipline
import Common.Packet
import Utility.Hash

class _Switch:
    def __init__(self,global_d=2, main_w=2**8, pipeline_number=4, port_per_pipe=4, delta_w=2**8):#xbar
        self.pipeline_number = pipeline_number
        self.port_per_pipe = port_per_pipe
        self.detlta_w = delta_w
        self.main_w = main_w
        self.ingress_pipeline = [Switch.IngressPipeline._Ingress_Pipeline(k=self.pipeline_number,w=delta_w,id=i,d=global_d,port_cnt=self.port_per_pipe) for i in range(0,self.pipeline_number)]
        #self.crossbar = xbar
        self.queue = [queue.Queue() for i in range(0,self.pipeline_number)]
        #self.queue = [Switch.SwitchQueue._Pipe_Queue(id=i) for i in range(0,self.pipeline_number)]
        self.egress_pipeline = [Switch.EgressPipline._Egress_Pipeline(k=self.pipeline_number,id=i,w=self.main_w,d=global_d) for i in range(0,self.pipeline_number)]
        
        self.hash = Utility.Hash._Hash()
        #self.queue_depth = []

        #处理数据包
    def Process_Packet(self, packet):
        in_pipe = packet.in_pipe
        out_pipe = packet.out_pipe
        g_packet = self.ingress_pipeline[in_pipe].Process_Pacekt(packet)
        self.queue[out_pipe].put(g_packet)
        if not self.queue[out_pipe].empty():
            self.egress_pipeline[out_pipe].Process_Pacekt(self.queue[out_pipe].get())

        #返回moniter pipeline的main sketch中的值
    def Query(self, flowID):
        moniter_pipe = self.hash.Hash_Function(str(flowID),self.pipeline_number,"SHA1")
        return self.egress_pipeline[moniter_pipe].Query(flowID)[0]

class _Single_Piplilne_Switch:
    def __init__(self,global_d=2, main_w=2**8):
        self.egress_pipeline = Switch.EgressPipline._Egress_Pipeline(k=1,id=0,w=main_w,d=global_d)
    
    #处理数据包
    def Process_Packet(self, packet):
        self.egress_pipeline.Process_Pacekt_Common(packet)
        
    #返回egresspipeline的main sketch中的值
    def Query(self, flowID):
        return self.egress_pipeline.Query(flowID)[0]

class _Parallel_Sketch:
    def __init__(self,global_d=2, main_w=2**8, pipeline_number=4, port_per_pipe=4):
        self.pipeline_number = pipeline_number
        self.egress_pipeline = [Switch.EgressPipline._Egress_Pipeline(k=self.pipeline_number,id=i,w=main_w,d=global_d) for i in range(0,self.pipeline_number)]
        self.port_per_pipe = port_per_pipe
    
    #处理数据包
    def Process_Packet(self, packet):
        out_pipe = packet.out_pipe
        self.egress_pipeline[out_pipe].Process_Pacekt_Common(packet)

        
    #返回所有egress_pipeline的main sketch中的值之和
    def Query(self, flowID):
        result = 0
        for i in range(0,self.pipeline_number):
            result += self.egress_pipeline[i].Query(flowID)[0]
        return result

class _Packet_Cache_Switch:
    def __init__(self, global_d=2, main_w=2**8, pipeline_number=4, port_per_pipe=4, queue_maxsize=0):
        self.pipeline_number = pipeline_number
        self.port_per_pipe = port_per_pipe
        self.main_w = main_w
        self.ingress_pipeline = [Switch.IngressPipeline._Packet_Cache_Ingress_Pipeline(k=self.pipeline_number,id=i,port_cnt=self.port_per_pipe,max_length=queue_maxsize) for i in range(0,self.pipeline_number)]
        #self.crossbar = xbar
        #self.queue = [Switch.SwitchQueue._Pipe_Queue(id=i) for i in range(0,self.pipeline_number)]
        self.egress_pipeline = [Switch.EgressPipline._Egress_Pipeline(k=self.pipeline_number,id=i,w=self.main_w,d=global_d) for i in range(0,self.pipeline_number)]
        
        self.hash = Utility.Hash._Hash()

    #处理数据包
    def Process_Packet(self, packet):
        in_pipe = packet.in_pipe
        out_pipe = packet.out_pipe
        #out_pipe = self.hash.Hash_Function(str(packet.flow.flowInfo.flowID),self.pipeline_number,"MD5")
        g_packet = self.ingress_pipeline[in_pipe].Process_Pacekt(packet)
        self.egress_pipeline[out_pipe].Process_Pacekt(g_packet)
        
    #返回所有egress_pipeline中的main sketch
    def Query(self, flowID):
        moniter_pipe = self.hash.Hash_Function(str(flowID),self.pipeline_number,"SHA1")
        return self.egress_pipeline[moniter_pipe].Query(flowID)[0]