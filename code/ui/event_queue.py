import threading

from code.ui.console import Console

class EventQueue(Console):
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()

    def add(self, event):
        self.queue.append(event)

    def get(self):
        event = self.queue.pop(0)
        return event

    def log(self, params):
        super().log(params)
        self.add(params)

    def is_empty(self):
        return len(self.queue) == 0

