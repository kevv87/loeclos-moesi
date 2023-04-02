import threading
from code.patterns.observer import PublisherRsvp

class Bus():
    def __init__(self, publisher_service=PublisherRsvp()):
        self.current_operation = None
        self.semaphore = threading.Semaphore()
        self.publisher_service = publisher_service

    def retrieve(self):
        return 5

    def store(self, operation):
        return True

    def read(self, operation):
        self.semaphore.acquire()
        self.publisher_service.notify_subscribers_rsvp(operation)
        result = self.retrieve()
        
        self.semaphore.release()

        return result

    def write(self, operation):
        self.semaphore.acquire()
        self.publisher_service.notify_subscribers(operation)
        result = self.retrieve()
        self.semaphore.release()

        return result

    def subscribe(self, subscriber):
        self.publisher_service.subscribe(subscriber)

