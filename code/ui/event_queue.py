import threading

class EventQueue():
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()

    def add(self, event):
        self.queue.append(event)

    def get(self):
        event = self.queue.pop(0)
        return event

    def log(self, params):
        self.lock.acquire()
        self.add(params)
        self.lock.release()

    def is_empty(self):
        return len(self.queue) == 0

