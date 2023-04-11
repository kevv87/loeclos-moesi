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
    def __init__(self, comm_bus, pause_event, op_queue, logger=Console()):
        threading.Thread.__init__(self)

        self.comm_bus = comm_bus
        self.processor_number = uuid.uuid4()
        self.stop_event = threading.Event()

        self.cache = Cache(self.processor_number, self.comm_bus, logger=logger)

        self.logger = logger
        log_params = [Events.PROCESSOR_CREATION, self.processor_number]
        logger.log(log_params)

        self.step = threading.Event()
        self.pause = pause_event

        self.op_queue = op_queue

    def create_calc_operation(self):
        return CalcOperation(self.processor_number, logger=self.logger)

    def create_write_operation(self):
        return WriteOperation(self.processor_number, logger=self.logger)

    def create_read_operation(self):
        return ReadOperation(self.processor_number, logger=self.logger)

    def manual_operation(self, operation):
        if operation.operation_type == "write":
            new_operation = WriteOperation(self.processor_number, logger=self.logger)
            new_operation.address = operation.address
            new_operation.data = operation.data
        elif operation.operation_type == "read":
            new_operation = ReadOperation(self.processor_number, logger=self.logger)
            new_operation.address = operation.address
        elif operation.operation_type == "calc":
            new_operation = CalcOperation(self.processor_number, logger=self.logger)

        return new_operation

    def choose_operation(self, random_number):
        if len(self.op_queue) > 0:
            print("Detected operation in q")
            operation = self.op_queue.pop(0)
            operation = self.manual_operation(operation)
        elif random_number == 1:
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

            if self.step.is_set():
                self.pause.set()
                self.step.clear()
            while(self.pause.is_set()):
                time.sleep(0.1)
                if self.step.is_set():
                    self.pause.clear()

    def stop(self):
        self.stop_event.set()

    def do_step(self):
        self.step.set()

