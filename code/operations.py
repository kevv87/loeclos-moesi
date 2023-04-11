from code.my_random import poisson_random_numbers

from code.ui.base import Events, Objects
from code.ui.console import Console

class Operation:
    operation_type = None
    def __init__(self, processor_number):
        self.processor_number = processor_number

class CalcOperation(Operation):
    operation_type = "calc"

    def __init__(self, processor_number, logger=Console()):
        super().__init__(processor_number)
        self.logger = logger
        log_params =\
            [Events.GENERATED_CALC_OPERATION,
             self.processor_number]
        self.logger.log(log_params)

class MemoryOperation(Operation):
    def __init__(self, processor_number):
        super().__init__(processor_number)
        self.address = poisson_random_numbers(5, 2, 0, 7)[0]
        self.miss = False

    def get_address(self):
        return bin(self.address)

class WriteOperation(MemoryOperation):
    operation_type = "write"
    def __init__(self, processor_number, logger=Console()):
        super().__init__(processor_number)
        self.data = poisson_random_numbers(5, 2, 0, 0xFFFF)[0]

        self.logger = logger
        log_params =\
            [Events.GENERATED_WRITE_OPERATION,
             self.processor_number, self.address, self.data]
        self.logger.log(log_params)

    def get_data(self):
        return hex(self.data)

class ReadOperation(MemoryOperation):
    operation_type = "read"

    def __init__(self, processor_number, logger=Console()):
        super().__init__(processor_number)

        log_params =\
            [Events.GENERATED_READ_OPERATION,
             self.processor_number, self.address]
        self.logger = logger
        self.logger.log(log_params)

class ResponseOperation(MemoryOperation):
    operation_type = "response"
    def __init__(self,processor_number, data, address, logger=Console()):
        super().__init__(processor_number)
        self.data = data
        self.address = address
        self.logger = logger

        log_params =\
            [Events.GENERATED_RESPONSE_OPERATION,
             self.processor_number, self.address, self.data]
        self.logger.log(log_params)

    def get_data(self):
        return hex(self.data)
