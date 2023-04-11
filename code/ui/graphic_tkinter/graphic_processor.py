import tkinter as tk
from tkinter import ttk

from code.operations import CalcOperation

class GraphicProcessor():
    def __init__(self, root, number, container):
        self.root = root
        self.number = number
        self.cache = [
            [0, 0, 0, "I"],
            [1, 0, 0, "I"],
            [2, 0, 0, "I"],
            [3, 0, 0, "I"],
        ]
        self.cache_labels = []
        self.operation = CalcOperation(self.number)
        self.test_counter = 0
        self.container = container

        self.create_frame()
        self.update_labels()

    def set_cache_block(self, idx, cache_block):
        self.cache[idx][1] = cache_block.address
        self.cache[idx][2] = cache_block.value
        self.cache[idx][3] = cache_block.state

    def create_frame(self):
        frame = tk.Frame(self.container, bd=1, relief="solid")

        label = tk.Label(frame, text=f"Processor {self.number}")
        label.pack(side="top", fill="x")

        self.operation_label = tk.Label(frame, text="Operation: {}".format(self.get_operation()))
        self.operation_label.pack(side="top", fill="x")

        for j in range(4):
            container = tk.Frame(frame)
            container.pack(side="top", fill="x")

            cache_to_write = self.cache[j]
            address = cache_to_write[1]
            value = cache_to_write[2]
            state = cache_to_write[3]

            tk.Label(container, text=f"Block {j}", width=10).pack(side="left")
            tk.Label(container, text="Address: {}".format(hex(address)), width=10).pack(side="left")
            tk.Label(container, text="Value: {}".format(bin(value)), width=10).pack(side="left")
            tk.Label(container, text="State: {}".format(state), width=10).pack(side="left")

        frame.pack(side="left", padx=10, pady=10)
        return frame

    def set_operation(self, operation):
        self.operation = operation

    def get_operation(self):
        op_type = self.operation.operation_type 
        string =\
            self.operation.operation_type + " "
        if op_type == "read":
            string += "from 0x" + hex(self.operation.address)
        elif op_type == "write":
            string += "0b" + bin(self.operation.value) + " to 0x" + hex(self.operation.address)

    def update_labels(self):
        self.test_counter += 1
        self.operation_label.config(text="Operation: {}".format(self.test_counter))
        self.root.after(1000, self.update_labels)
