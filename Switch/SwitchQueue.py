# 继承Queue类，queue id与ingress/egress pipeline一致
import queue

class _Pipe_Queue(queue.Queue):
    def __init__(self, id):
        self.queue_id = id
    
