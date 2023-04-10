#
import queue

class _Egress_Queue(queue.Queue):
    def __init__(self, id):
        self.queue_id = id
    
