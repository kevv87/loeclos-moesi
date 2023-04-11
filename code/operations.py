from code.my_random import poisson_random_numbers

class Operation:
    operation_type = None
    def __init__(self, processor_number):
        self.processor_number = processor_number

class CalcOperation(Operation):
    operation_type = "calc"

class MemoryOperation(Operation):
    def __init__(self, processor_number):
        super().__init__(processor_number)
        self.address = poisson_random_numbers(5, 2, 0, 7)[0]
        self.miss = False

    def get_address(self):
        return bin(self.address)

class WriteOperation(MemoryOperation):
    operation_type = "write"
    def __init__(self, processor_number):
        super().__init__(processor_number)
        self.data = poisson_random_numbers(5, 2, 0, 0xFFFF)[0]

    def get_data(self):
        return hex(self.data)

class ReadOperation(MemoryOperation):
    operation_type = "read"

class ResponseOperation(MemoryOperation):
    operation_type = "response"
    def __init__(self,processor_number, data, address):
        super().__init__(processor_number)
        self.data = data
        self.address = address

    def get_data(self):
        return hex(self.data)
