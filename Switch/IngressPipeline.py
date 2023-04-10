# ingress pipeline类
import Sketch.CMSketch
class _Ingress_Pipeline:
    def __init__(self, k, w, d=2) -> None:
        self.pipeline_number = k
        self.pipeline_id = -1
        self.port = []  # 对应的输入端口
        self.pipeline_table = []
        self.w = w
        self.d = d
        self.delta_sketch = None

    # 初始化ingress pipeline的信息以及pipeline table和delta sketch
    def Init_Ingress_Pipeline(self):
        pass
    
    # 处理接收的包并发送给cross bar
    def Process_Pacekt(self, packet):
        pass