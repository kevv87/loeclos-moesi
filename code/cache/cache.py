from code.constants import *
from code.cache.constants import *
from code.cache.moesi import Moesi
from code.patterns.observer import SubscriberRsvp

from code.operations import ResponseOperation

import pdb

class CacheBlock():
    def __init__(self, number):
        self.number = number
        self.state = MoesiStates.I
        self.data = 0
        self.mem_address = 0

class Cache(SubscriberRsvp):
    def __init__(self, coherencyService = Moesi()):
        self.contents = [CacheBlock(0), CacheBlock(1), CacheBlock(2), CacheBlock(3)]
        self.coherencyService = coherencyService

    def process_read_notification(self, operation):
        matching_block = self.find_block(operation)

        if matching_block:
            matching_block.state =\
                    self.get_next_state(matching_block.state, MoesiEvents.OTHERS_READ)

    def process_write_notification(self, operation):
        matching_block = self.find_block(operation)

        if matching_block:
            matching_block.state =\
                    self.get_next_state(matching_block.state, MoesiEvents.OTHERS_WRITE)

    def notify(self, msg=None):
        if msg.operation_type == "read":
            self.process_read_notification(msg)
        elif msg.operation_type == "write":
            self.process_write_notification(msg)
        else:
            print("Unknown operation type: " + msg.operation_type)

    def notify_rsvp(self, msg=None):
        pass

    def run_substitution_policy(self, subset):
        i = 0
        modified = []
        owned = []
        exclusive = []
        shared = []
        invalid = []
        
        for block in subset:
            if block.state == MoesiStates.M:
                modified.append(i)
            elif block.state == MoesiStates.O:
                owned.append(i)
            elif block.state == MoesiStates.E:
                exclusive.append(i)
            elif block.state == MoesiStates.S:
                shared.append(i)
            elif block.state == MoesiStates.I:
                invalid.append(i)
            i += 1

        if len(invalid) > 0:
            return invalid[0]
        elif len(shared) > 0:
            return shared[0]
        elif len(exclusive) > 0:
            return exclusive[0]
        elif len(modified) > 0:
            return modified[0]
        elif len(owned) > 0:
            return owned[0]

    def find_idx_to_replace(self, operation):
        set_to_replace = operation.address % 2
        set_size = len(self.contents) / 2

        subset_from = int(set_to_replace * set_size)
        subset_to = int((set_to_replace + 1) * set_size)
        subset = self.contents[subset_from : subset_to]
        offset = self.run_substitution_policy(subset)

        idx_to_replace = int(set_to_replace * set_size + offset)

        return idx_to_replace

    def read_from_bus(self, operation, test_exclusive=False):
        # Retrieve data from bus
        responseOp = ResponseOperation(1, 2)
        if test_exclusive:
            responseOp = ResponseOperation(PROCESSOR_NUMBER_MEMORY, 2)
        comes_from_memory = responseOp.processor_number == PROCESSOR_NUMBER_MEMORY
        return (responseOp.data, comes_from_memory)

    def get_next_state(self, current_state, action):
        return self.coherencyService.compute_next_state(current_state, action)

    def find_block(self, operation):
        found_block = False

        for block in self.contents:
            if block.mem_address == operation.address and block.state != MoesiStates.I:
                found_block = block
                break

        return found_block

    def write(self, operation):
        matching_block = self.find_block(operation)

        if matching_block:
            matching_block.data = operation.data
            matching_block.state =\
                    self.get_next_state(
                            matching_block.state,
                            MoesiEvents.SELF_WRITE )
        else:
            idx_to_replace = self.find_idx_to_replace(operation)
            
            self.contents[idx_to_replace].data = operation.data
            self.contents[idx_to_replace].mem_address = operation.address
            self.contents[idx_to_replace].state =\
                    self.get_next_state(
                            self.contents[idx_to_replace].state,
                            MoesiEvents.SELF_WRITE )

    def read(self, operation):
        matching_block = self.find_block(operation)

        if matching_block:
            return matching_block.data
        else:
            # TODO: If not found, is miss and should fetch it and then replace it in
            # the cache
            # TODO: Go to bus
            (data, comes_from_memory) = self.read_from_bus(operation)
            if operation.address == 10:
                (data, comes_from_memory) = self.read_from_bus(operation, test_exclusive=True)
            idx_to_replace = self.find_idx_to_replace(operation)

            self.contents[idx_to_replace].data = data
            self.contents[idx_to_replace].mem_address = operation.address

            if comes_from_memory:
                action = MoesiEvents.EXCLUSIVE_READ
            else:
                action = MoesiEvents.SELF_READ

            self.contents[idx_to_replace].state =\
                    self.get_next_state(
                            self.contents[idx_to_replace].state,
                            action )

            return data

