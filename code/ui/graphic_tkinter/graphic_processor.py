import tkinter as tk
from tkinter import ttk

from code.operations import CalcOperation

class GraphicProcessor():
    def __init__(self, root, number, container):
        self.root = root
        self.number = number
        self.operation = None
        self.last_operation = None
        self.cache = [
            [0, 0, 0, "I"],
            [1, 0, 0, "I"],
            [2, 0, 0, "I"],
            [3, 0, 0, "I"],
        ]
        self.cache_labels = []
        self.test_counter = 0
        self.container = container

        self.create_frame()
        self.update()

    def set_cache_block(self, idx, cache_block):
        self.cache[idx][1] = cache_block.mem_address
        self.cache[idx][2] = cache_block.data
        self.cache[idx][3] = cache_block.state.value

    def create_frame(self):
        frame = tk.Frame(self.container, bd=1, relief="solid")

        self.proc_label = tk.Label(frame, text=f"Processor {self.number}")
        self.proc_label.pack(side="top", fill="x")


        self.last_operation_label = tk.Label(frame, text="Last Operation: None")
        self.last_operation_label.pack(side="top", fill="x")

        self.operation_label = tk.Label(frame, text="Operation: {}".format(self.get_operation()))
        self.operation_label.pack(side="top", fill="x")

        for j in range(4):
            container = tk.Frame(frame)
            container.pack(side="top", fill="x")

            cache_to_write = self.cache[j]
            address = cache_to_write[1]
            value = cache_to_write[2]
            state = cache_to_write[3]

            this_cache_labels = []
            block_label = tk.Label(container, text=f"Block {j}", width=10)
            block_label.pack(side="left")
            this_cache_labels.append(block_label)

            address_label = tk.Label(container, text="Address: {}".format(bin(address)), width=10)
            address_label.pack(side="left")
            this_cache_labels.append(address_label)

            value_label = tk.Label(container, text="Value: {}".format(hex(value)), width=10)
            value_label.pack(side="left")
            this_cache_labels.append(value_label)
            
            state_label = tk.Label(container, text="State: {}".format(state), width=10)
            state_label.pack(side="left")
            this_cache_labels.append(state_label)
            
            self.cache_labels.append(this_cache_labels)

        frame.pack(side="left", padx=10, pady=10)
        return frame

    def set_id(self, processor_id):
        self.number = processor_id

    def set_operation(self, operation):
        self.last_operation = self.operation
        self.operation = operation

    def get_last_operation(self):
        if not self.last_operation:
            return "None"

        op_type = self.last_operation.operation_type 
        string =\
            self.last_operation.operation_type + " "
        if op_type == "read":
            string += "from " + hex(self.last_operation.address)
        elif op_type == "write":
            string +=  bin(self.last_operation.data) + " to " + hex(self.last_operation.address)

        return string

    def get_operation(self):
        if not self.operation:
            return "None"

        op_type = self.operation.operation_type 
        string =\
            self.operation.operation_type + " "
        if op_type == "read":
            string += "from " + hex(self.operation.address)
        elif op_type == "write":
            string +=  bin(self.operation.data) + " to " + hex(self.operation.address)

        return string

    def update_cache_labels(self):
        for cache_values in self.cache:
            idx = cache_values[0]
            address = cache_values[1]
            value = cache_values[2]
            state = cache_values[3]

            self.cache_labels[idx][1].config(text="Address: {}".format(hex(address)))
            self.cache_labels[idx][2].config(text="Value: {}".format(bin(value)))
            self.cache_labels[idx][3].config(text="State: {}".format(state))

    def update(self):
        print("Called update")
        self.proc_label.config(text=f"Processor {self.number}")
        self.last_operation_label.config(text="Last Operation: {}".format(self.get_last_operation()))
        self.operation_label.config(text="Operation: {}".format(self.get_operation()))

        self.update_cache_labels()

