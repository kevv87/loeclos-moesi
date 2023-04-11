import threading
import uuid
import time

from code.operations import CalcOperation, WriteOperation, ReadOperation
from code.my_random import poisson_random_numbers
from code.processors.constants import *
from code.cache.cache import Cache

from code.ui.base import Events, Objects
from code.ui.console import Console

class Processor(threading.Thread):
    def __init__(self, comm_bus, logger=Console()):
        threading.Thread.__init__(self)

        self.comm_bus = comm_bus
        self.processor_number = uuid.uuid4()
        self.stop_event = threading.Event()

        self.cache = Cache(self.processor_number, self.comm_bus, logger=logger)

        self.logger = logger
        log_params = [Events.PROCESSOR_CREATION, self.processor_number]
        logger.log(log_params)

    def create_calc_operation(self):
        return CalcOperation(self.processor_number, logger=self.logger)

    def create_write_operation(self):
        return WriteOperation(self.processor_number, logger=self.logger)

    def create_read_operation(self):
        return ReadOperation(self.processor_number, logger=self.logger)

    def choose_operation(self, random_number):
        if random_number == 1:
            operation = self.create_calc_operation()
        elif random_number == 2:
            operation = self.create_write_operation()
        elif random_number == 3:
            operation = self.create_read_operation()
        else:
            raise Exception("Number to choose out of bounds")
        return operation

    def run(self):
        while not self.stop_event.is_set():
            random_number = poisson_random_numbers(5, 2, 1, 3)[0]
            operation = self.choose_operation(random_number)

            if operation.operation_type == "write":
                self.cache.write(operation)
            elif operation.operation_type == "read":
                self.cache.read(operation)

            time.sleep(PROCESSOR_ACTION_SECONDS)

    def stop(self):
        self.stop_event.set()

