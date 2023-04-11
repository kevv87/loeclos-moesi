from code.ui.base import Events, Objects

class Console():
    def log_creation(self, created_object):
        print("Created {}".format(created_object))

    def log_generated_calc_operation(self, processor_number):
        print("Processor {} generated a calc operation".format(processor_number))

    def log_generated_write_operation(self, processor_number, address, value):
        print("Processor {} generated a write operation to address {} with value {}".format(processor_number, address, value))

    def log_generated_read_operation(self, processor_number, address):
        print("Processor {} generated a read operation to address {}".format(processor_number, address))

    def log(params):
        action = params[0]

        if action == Events.CREATION:
            self.log_creation(params[1])
        elif action == Events.GENERATED_CALC_OPERATION:
            self.log_generated_calc_operation(params[1])
        elif action == Events.GENERATED_WRITE_OPERATION:
            self.log_generated_write_operation(params[1], params[2], params[3])
        elif action == Events.GENERATED_READ_OPERATION:
            self.log_generated_read_operation(params[1], params[2])
