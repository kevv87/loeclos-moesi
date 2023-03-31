import time

from code.memory.constants import *
from code.memory.error_types import SegmentationFault, DataOverflow

class Memory():
    def __init__(self):
        self.contents = [0] * MEMORY_BLOCK_WIDTH
        self.bit_depth = MEMORY_BLOCK_DEPTH_BITS

    def is_data_within_bounds(self, data):
        max_val = (1 << (self.bit_depth - 1)) - 1
        min_val = -max_val - 1
        return min_val <= data <= max_val

    def validate_address(self, address):
        if address >= MEMORY_BLOCK_WIDTH or address < 0:
            raise SegmentationFault("Trying to access memory address: {}, which is out of bounds".format(address))

    def validate_data(self, data, address):
        if not self.is_data_within_bounds(data):
            raise DataOverflow("Trying to add data: {} to memory address: {} that is too large".format(data, address))

    def memory_access(self, address, data, write, real_time=True):
        self.validate_address(address)

        if real_time:
            time.sleep(MEMORY_ACCESS_SECONDS)

        if write:
            self.validate_data(data, address)
            self.contents[address] = data

        return self.contents[address]

    def add_data(self, address, data, real_time=True):
        self.memory_access(address, data, True, real_time)

    def read_data(self, address, real_time=True):
        return self.memory_access(address, None, False, real_time)

    def visualize(self):
        return self.contents

