#
import queue

class _Pipe_Cache(queue.Queue):
    def __init__(self, id):
        self.cache_id = id