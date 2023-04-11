from code.ui.base import Events, Objects

class Console():
    def log_proc_creation(self, processor_number):
        print("·· Created processor {}".format(processor_number))

    def log_generated_calc_operation(self, processor_number):
        print("·· Processor {}: generated a calc operation".format(processor_number))

    def log_generated_write_operation(self, processor_number, address, value):
        print("·· Processor {}: generated a write operation to address {} with value {}".format(processor_number, address, value))

    def log_generated_read_operation(self, processor_number, address):
        print("·· Processor {}: generated a read operation to address {}".format(processor_number, address))

    def log_cache_read(self, processor_number, address):
        print("·· Processor {}: polls its cache for address {}".format(processor_number, address))

    def log_cache_hit(self, processor_number, block_number, address, value, state):
        print("·· Processor {}: found block {} with address {} and value {} will have state {}".format(processor_number, block_number, address, value, state))

    def log_cache_miss(self, processor_number, address):
        print("·· Processor {}: cache miss on address {}".format(processor_number, address))

    def log_cache_requesting_value_bus(self, processor_number, address):
        print("·· Processor {}: requesting bus for address {}".format(processor_number, address))

    def log_cache_gives_response(self, giving_processor):
        print("·· Bus: processor {} gives requested address".format(giving_processor))

    def log_cache_retrieving_from_memory(self, address, data):
        print("·· Bus: data retrieved from memory, address: {}, value: {}".format(address, data))

    def log_replacing_block(self, processor_number, block_number, address, value, state):
        print("·· Processor {}: replacing block {} with address {} and value {}, new state {}".format(processor_number, block_number, address, value, state))

    def log_writing_block(self, processor_number, block_number, address, value, state):
        print("·· Processor {}: writing block {} with address {} and value {}, new state {}".format(processor_number, block_number, address, value, state))

    def log_writeback(self, processor_number, address, value):
        print("·· Processor {}: writeback to memory, address: {}, value: {}".format(processor_number, address, value))

    def log_updating_block(self, processor_number, block_number, address, value, state):
        print("·· Processor {}: updating block {} with address {} and value {}, new state {}".format(processor_number, block_number, address, value, state))

    def log(self, params):
        action = params[0]

        if action == Events.PROCESSOR_CREATION:
            self.log_proc_creation(params[1])
        elif action == Events.GENERATED_CALC_OPERATION:
            self.log_generated_calc_operation(params[1])
        elif action == Events.GENERATED_WRITE_OPERATION:
            self.log_generated_write_operation(params[1], params[2], params[3])
        elif action == Events.GENERATED_READ_OPERATION:
            self.log_generated_read_operation(params[1], params[2])
        elif action == Events.CACHE_READ:
            self.log_cache_read(params[1], params[2])
        elif action == Events.CACHE_HIT:
            self.log_cache_hit(params[1], params[2], params[3], params[4], params[5])
        elif action == Events.CACHE_MISS:
            self.log_cache_miss(params[1], params[2])
        elif action == Events.CACHE_REQUESTING_VALUE_BUS:
            self.log_cache_requesting_value_bus(params[1], params[2])
        elif action == Events.CACHE_GIVES_RESPONSE:
            self.log_cache_gives_response(params[1])
        elif action == Events.RETRIEVING_FROM_MEMORY:
            self.log_cache_retrieving_from_memory(params[1], params[2])
        elif action == Events.REPLACING_BLOCK:
            self.log_replacing_block(params[1], params[2], params[3], params[4], params[5])
        elif action == Events.WRITING_BLOCK:
            self.log_writing_block(params[1], params[2], params[3], params[4], params[5])
        elif action == Events.WRITEBACK:
            self.log_writeback(params[1], params[2], params[3])
        elif action == Events.UPDATING_BLOCK:
            self.log_updating_block(params[1], params[2], params[3], params[4], params[5])
