import time

from code.constants import *
from code.cache.constants import *
from code.cache.moesi import Moesi
from code.patterns.observer import SubscriberRsvp

from code.operations import ResponseOperation, Operation

from code.ui.base import Events, Objects
from code.ui.console import Console

import pdb

class CacheBlock():
    def __init__(self, number):
        self.number = number
        self.state = MoesiStates.I
        self.data = 0
        self.mem_address = 0

class Cache(SubscriberRsvp):
    def __init__( self, my_processor_number,
            bus, coherencyService = Moesi(), logger = Console(), realTime=True) :
        super().__init__()
        self.contents = [CacheBlock(0), CacheBlock(1), CacheBlock(2), CacheBlock(3)]
        self.bus = bus
        self.coherencyService = coherencyService
        self.processor_number = my_processor_number

        self.can_answer_with_shared = False
        self.logger = logger
        self.realTime = realTime

        self.waiting_for_block = None

    def process_read_notification(self, operation):
        matching_block = self.find_block(operation)

        if matching_block:
            self.change_state(matching_block, operation, MoesiEvents.OTHERS_READ)

    def change_state(self, block, operation, moesiEvent):
        previous_state = block.state
        next_state =\
            self.get_next_state(block.state, moesiEvent)

        if ( ( previous_state == MoesiStates.M or previous_state == MoesiStates.O )
                and next_state == MoesiStates.I ):
            self.bus.writeBack(operation)

        block.state = next_state
        log_params = [
            Events.UPDATING_BLOCK,
            self.processor_number, block.number,
            block.mem_address, block.data, block.state ]
        self.logger.log(log_params)

    def process_write_notification(self, operation):
        matching_block = self.find_block(operation)

        if matching_block:
            self.change_state(matching_block, operation, MoesiEvents.OTHERS_WRITE)

    def notify(self, msg=None):
        if msg.processor_number == self.processor_number:
            return
        elif msg.operation_type == "read":
            self.process_read_notification(msg)
        elif msg.operation_type == "write":
            self.process_write_notification(msg)
        elif msg.operation_type == "response":
            if self.can_answer_with_shared:
                self.can_answer_with_shared = False
        else:
            print("Unknown operation type: " + msg.operation_type)

    def answer_with_shared(self, matching_block):
        if not matching_block:
            return False
        if self.can_answer_with_shared:
            responseOperation =\
                ResponseOperation(
                        self.processor_number, matching_block.data,
                        matching_block.mem_address )

            self.can_answer_with_shared = False
            self.waiting_for_block = None

            return responseOperation
        else: 
            self.waiting_for_block = matching_block
            self.can_answer_with_shared = True
            return False

    def process_rsvp(self, operation):
        matching_block = self.find_block(operation)

        if matching_block:
            if ( matching_block.state == MoesiStates.O or
                matching_block.state == MoesiStates.E or 
                matching_block.state == MoesiStates.M ):
                responseOperation =\
                    ResponseOperation(
                            self.processor_number, matching_block.data,
                            matching_block.mem_address )
                return responseOperation
            elif matching_block.state == MoesiStates.S:
                return self.answer_with_shared(matching_block)

        return False

    def find_operation_in_array(self, array):
        for element in array:
            if isinstance(element, Operation):
                return element

    def notify_rsvp(self, msg=None):
        if not isinstance(msg, Operation):
            found_operation = self.find_operation_in_array(msg)
            if not found_operation:
                return self.answer_with_shared(self.waiting_for_block)
            else:
                self.can_answer_with_shared = False
                self.waiting_for_block = None
                return False
        elif msg.operation_type == "read":
            responseOperation = self.process_rsvp(msg)
            self.process_read_notification(msg)
            return responseOperation

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

    def read_from_bus(self, operation):
        operation.miss = True
        log_params = [
            Events.CACHE_REQUESTING_VALUE_BUS, self.processor_number, operation.address]
        self.logger.log( log_params )

        responseOp = self.bus.read(operation)

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

            if self.realTime:
                time.sleep(CACHE_ACCESS_SECONDS)
            log_params = [
                    Events.UPDATING_BLOCK, self.processor_number, matching_block.number,
                    matching_block.mem_address, matching_block.data,
                    matching_block.state ]
            self.logger.log(log_params)
        else:
            idx_to_replace = self.find_idx_to_replace(operation)
            self.evict(idx_to_replace)
            
            self.contents[idx_to_replace].data = operation.data
            self.contents[idx_to_replace].mem_address = operation.address
            self.contents[idx_to_replace].state =\
                    self.get_next_state(
                            self.contents[idx_to_replace].state,
                            MoesiEvents.SELF_WRITE )
            if self.realTime:
                time.sleep(CACHE_ACCESS_SECONDS)
            log_params = [
                    Events.WRITING_BLOCK, self.processor_number,
                    self.contents[idx_to_replace].number,
                    self.contents[idx_to_replace].mem_address,
                    self.contents[idx_to_replace].data,
                    self.contents[idx_to_replace].state ]
            self.logger.log(log_params)

    def evict(self, idx_to_evict):
        if self.contents[idx_to_evict].state == MoesiStates.M:
            writebackOperation = ResponseOperation(
                    self.processor_number, self.contents[idx_to_evict].data,
                    self.contents[idx_to_evict].mem_address )
            self.bus.writeBack(writebackOperation)
    
    def read(self, operation):
        log_params = [Events.CACHE_READ, self.processor_number, operation.address]
        self.logger.log(log_params)

        matching_block = self.find_block(operation)

        if matching_block:
            if self.realTime:
                time.sleep(CACHE_ACCESS_SECONDS)
            log_params = [
                    Events.CACHE_HIT, self.processor_number, matching_block.number,
                    matching_block.mem_address, matching_block.data,
                    matching_block.state]
            self.logger.log(log_params)

            return matching_block.data
        else:
            log_params = [Events.CACHE_MISS, self.processor_number, operation.address]
            self.logger.log(log_params)

            (data, comes_from_memory) = self.read_from_bus(operation)
            idx_to_replace = self.find_idx_to_replace(operation)
            self.evict(idx_to_replace)

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
            if self.realTime:
                time.sleep(CACHE_ACCESS_SECONDS)
            log_params = [
                    Events.REPLACING_BLOCK, self.processor_number,
                    self.contents[idx_to_replace].number,
                    self.contents[idx_to_replace].mem_address,
                    self.contents[idx_to_replace].data,
                    self.contents[idx_to_replace].state]
            self.logger.log(log_params)

            return data

