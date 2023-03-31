class Operation:
    operation_type = None
    def __init__(self, processor_number):
        self.processor_number = processor_number

class CalcOperation(Operation):
    operation_type = "calc"

class MemoryOperation(Operation):
    address = 5

    def get_address(self):
        return bin(self.address)

class WriteOperation(MemoryOperation):
    operation_type = "write"
    data = 18

    def get_data(self):
        return hex(self.data)

class ReadOperation(MemoryOperation):
    operation_type = "read"
