import threading
from code.patterns.observer import PublisherRsvp
from code.operations import ResponseOperation
from code.constants import *

from code.ui.base import Events, Objects
from code.ui.console import Console

class Bus():
    def __init__(self, memory, publisher_service=PublisherRsvp(), logger=Console()):
        self.semaphore = threading.Semaphore()
        self.publisher_service = publisher_service
        self.memory = memory

        self.logger = logger

    def retrieve(self, operation):
        data = self.memory.read_data(operation.address)
        response = ResponseOperation(PROCESSOR_NUMBER_MEMORY, operation.address, data)

        logger_params =\
            [Events.RETRIEVING_FROM_MEMORY, response.address, response.data]
        self.logger.log(logger_params)

        return response

    def store(self, operation):
        return self.memory.write_data(operation.address, operation.data)

    def search_in_caches(self, caches_response):
        for response in caches_response:
            if response:
                return True

    def take_first_cache_response(self, caches_response):
        for response in caches_response:
            if response:
                return response

    def read(self, operation):
        self.semaphore.acquire()

        caches_response = self.publisher_service.notify_subscribers_rsvp(operation)

        if operation.miss:
            found_in_caches = self.search_in_caches(caches_response)
            if found_in_caches:
                result = self.take_first_cache_response(caches_response)

                log_params =\
                    [Events.CACHE_GIVES_RESPONSE, result.processor_number]
                self.logger.log(log_params)

                self.publisher_service.notify_subscribers(result)
                self.semaphore.release()
                return result
            else:
                caches_response = self.publisher_service.notify_subscribers_rsvp(caches_response)
                found_in_caches = self.search_in_caches(caches_response)
                if found_in_caches:
                    result = self.take_first_cache_response(caches_response)
                    log_params =\
                        [Events.CACHE_GIVES_RESPONSE, result.processor_number]
                    self.logger.log(log_params)
                    self.semaphore.release()
                    return result
                else:
                    result = self.retrieve(operation)
        else:
            result = operation
        
        self.semaphore.release()

        return result

    def write(self, operation):
        print("Acquiring semaphore to write")
        self.semaphore.acquire()
        self.publisher_service.notify_subscribers(operation)
        print("Releasing semaphore after write")
        self.semaphore.release()

    def writeBack(self, operation):
        self.semaphore.acquire()
        self.store(operation)
        self.semaphore.release()
        
        log_params = [
            Events.WRITEBACK, operation.processor_number,
            operation.address, operation.data,
        ]
        self.logger.log(log_params)
    
    def subscribe(self, subscriber):
        self.publisher_service.subscribe(subscriber)

    def unsubscribeAll(self):
        self.publisher_service.unsubscribeAll()

