import threading
from code.patterns.observer import Publisher

class Bus():
    def __init__(self, publisher_service=Publisher()):
        self.current_operation = None
        self.semaphore = threading.Semaphore()
        self.publisher_service = publisher_service

    def add_operation(self, operation):
        self.semaphore.acquire()
        self.publisher_service.notify_subscribers()
        self.current_operation = operation

    def pop_operation(self):
        self.semaphore.release()
        operation = self.current_operation
        self.current_operation = None
        return operation
