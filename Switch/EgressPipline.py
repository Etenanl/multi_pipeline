# egress pipeline类
import Sketch.ElasticSketch
import Switch.Queue
class _Egress_Pipeline:
    def __init__(self, k, h, w, d=2) -> None:
        self.pipeline_number = k
        self.pipeline_id = -1
        self.port = []  # 对应的输出端口
        self.h = h
        self.w = w
        self.d = d
        self.delta_sketch = None
        self.packet_queue = None

    # 初始化egress pipeline的信息以及main sketch和queue
    def Init_Egress_Pipeline(self):
        pass
    
    # 从队列中接收并处理包，读取其中的metadata信息，然后将包发送给出口port
    def Process_Pacekt(self, packet):
        pass