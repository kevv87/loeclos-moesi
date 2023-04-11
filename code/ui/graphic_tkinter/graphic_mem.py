import tkinter as tk
from tkinter import ttk

class GraphicMemory():
    def __init__(self, root):
        self.root = root
        self.contents = [
            [i, 0] for i in range(8) ]
        self.mem_labels = []
        self.create_frame()

    def set_value(self, address, value):
        self.contents[address][1] = value
        self.update()

    def update(self):
        for i in range(8):
            address = self.contents[i][0]
            data = self.contents[i][1]

            address_label = self.mem_labels[i][0]
            address_label.configure(text="Address: {}".format(bin(address)))

            data_label = self.mem_labels[i][1]
            data_label.configure(text="Data: {}".format(hex(data)))

    def create_frame(self):
        frame = tk.Frame(self.root, bd=1, relief="solid")
        title = tk.Label(frame, text="Memory")
        title.pack(side="top", fill="x")

        for i in range(8):
            container = tk.Frame(frame)
            container.pack(side="top", fill="x")

            address = self.contents[i][0]
            data = self.contents[i][1]

            this_mem_labels = []
            address_label = tk.Label(container, text="Address: {}".format(hex(address)))
            address_label.pack(side="left")
            this_mem_labels.append(address_label)

            data_label = tk.Label(container, text="Data: {}".format(bin(data)))
            data_label.pack(side="left")
            this_mem_labels.append(data_label)

            self.mem_labels.append(this_mem_labels)

        frame.pack(side="left", padx=10, pady=10)
        return frame

