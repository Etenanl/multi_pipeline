import Switch.IngressPipeline
import Switch.Crossbar
import Switch.Queue
import Switch.EgressPipline
import Switch.PipeCache
import Common.Packet

class _Switch:
    def __init__(self, in_pipeline, xbar, queue, e_pipeline):
        self.ingress_pipeline = in_pipeline
        self.crossbar = xbar
        self.queue = queue
        self.egress_pipeline = e_pipeline
        #self.queue_depth = []

        #处理数据包
        def Process_Packet(self, packet):
            pass
        
        #返回所有egress_pipeline中的main sketch
        def Query(self):
            pass

class _Single_Piplilne_Switch:
    def __init__(self, e_pipeline):
        self.egress_pipeline = e_pipeline
    
    #处理数据包
    def Process_Packet(self, packet):
        pass
        
    #返回所有egress_pipeline中的main sketch
    def Query(self):
        pass

class _Parallel_Sketch:
    def __init__(self, e_pipeline):
        self.egress_pipeline = e_pipeline
    
    #处理数据包
    def Process_Packet(self, packet):
        pass
        
    #返回所有egress_pipeline中的main sketch
    def Query(self):
        pass

class _Packet_Cache_Switch:
    def __init__(self, pipecache, e_pipeline):
        self.pipe_cache = pipecache
        self.egress_pipeline = e_pipeline

    #处理数据包
    def Process_Packet(self, packet):
        pass
        
    #返回所有egress_pipeline中的main sketch
    def Query(self):
        pass