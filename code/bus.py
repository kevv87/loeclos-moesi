import threading
from code.patterns.observer import PublisherRsvp
from code.operations import ResponseOperation
from code.constants import *

class Bus():
    def __init__(self, memory, publisher_service=PublisherRsvp()):
        self.semaphore = threading.Semaphore()
        self.publisher_service = publisher_service
        self.memory = memory

    def retrieve(self, operation):
        data = self.memory.read_data(operation.address)
        response = ResponseOperation(PROCESSOR_NUMBER_MEMORY, data)
        return response

    def store(self, operation):
        return self.memory.write_data(operation.address, operation.data)

    def search_in_caches(self, caches_response):
        for response in caches_response:
            if response:
                return True

    def read(self, operation):
        self.semaphore.acquire()

        caches_response = self.publisher_service.notify_subscribers_rsvp(operation)

        if operation.miss:
            found_in_caches = self.search_in_caches(caches_response)
            if found_in_caches:
                result = caches_response[0]
                self.publisher_service.notify_subscribers(result)
                return result
            else:
                caches_response = self.publisher_service.notify_subscribers_rsvp(caches_response)
                found_in_caches = self.search_in_caches(caches_response)
                if found_in_caches:
                    return caches_response[0]
                else:
                    result = self.retrieve(operation)
        else:
            result = operation
        
        self.semaphore.release()

        return result

    def write(self, operation):
        self.semaphore.acquire()
        self.publisher_service.notify_subscribers(operation)
        result = self.retrieve(operation)
        self.semaphore.release()

        return result

    def writeBack(self, operation):
        self.semaphore.acquire()
        self.store(operation)
        self.semaphore.release()
    
    def subscribe(self, subscriber):
        self.publisher_service.subscribe(subscriber)

    def unsubscribeAll(self):
        self.publisher_service.unsubscribeAll()

