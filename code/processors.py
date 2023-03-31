import threading
import uuid
import time
from code.operations import CalcOperation, WriteOperation, ReadOperation
from code.my_random import poisson_random_numbers


class Processor(threading.Thread):
    def __init__(self, comm_bus):
        threading.Thread.__init__(self)

        self.comm_bus = comm_bus
        self.processor_number = uuid.uuid4()
        self.stop_event = threading.Event()

    def create_calc_operation(self):
        return CalcOperation(self.processor_number) 

    def create_write_operation(self):
        return WriteOperation(self.processor_number)

    def create_read_operation(self):
        return ReadOperation(self.processor_number)

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
        print("### Starting Processor ###")
        while not self.stop_event.is_set():
            random_number = poisson_random_numbers(5, 2, 1, 3)[0]
            operation = self.choose_operation(random_number)
            self.comm_bus.append(operation)

            time.sleep(0.5)

    def stop(self):
        self.stop_event.set()

