# crossbar将一个ingress pipeline的数据包传输给一个egress pipeline
# 可以直接把包从ingress pipeline传送到queue

class _Crossbar:
    def __init__(self) -> None:
        pass
    
    # 将数据包传送给对应egress pipeline的queue
    def Cross_Send_packet(self, packet, queue_id):
        pass