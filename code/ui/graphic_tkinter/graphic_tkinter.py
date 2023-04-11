import time
import tkinter as tk
from tkinter import ttk

from code.operations import CalcOperation, WriteOperation, ReadOperation
from code.cache.cache import CacheBlock

from code.ui.graphic_tkinter.graphic_processor import GraphicProcessor
from code.ui.graphic_tkinter.graphic_mem import GraphicMemory
from code.ui.base import Events, Objects
from code.ui.console import NoLogger

class GUI():
    def creating_processors(self):
        # Create a container for the processors with a scrollbar
        container = tk.Frame(self.root)
        container.pack(side="top", fill="both", expand=True)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=scrollbar.set)

        # Pack the scrollbar and canvas
        scrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="top", fill="both", expand=True)

        # Create a Frame to hold the processors
        processors_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=processors_frame, anchor="nw")
        self.last_processor = 0

        self.processors = []
        for i in range(4):
            graphic_proc = GraphicProcessor(self.root, i, processors_frame)
            self.processors.append(graphic_proc)

        processors_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def creating_memory(self):
        self.graphic_memory = GraphicMemory(self.root)

    def search_processor_by_id(self, proc_id):
        for proc in self.processors:
            if proc.number == proc_id:
                return proc
        return None
    
    def handle_event(self, event):
        action = event[0]
        if action == Events.PROCESSOR_CREATION:
            graphic_processor = self.processors[self.last_processor]
            graphic_processor.set_id(event[1])
            self.last_processor += 1
        elif action == Events.GENERATED_CALC_OPERATION:
            graphic_processor = self.search_processor_by_id(event[1])
            calc_operation = CalcOperation(event[1], logger=NoLogger())
            graphic_processor.set_operation(calc_operation)
        elif action == Events.GENERATED_WRITE_OPERATION:
            graphic_processor = self.search_processor_by_id(event[1])
            write_operation = WriteOperation(event[1], logger=NoLogger())
            write_operation.address = event[2]
            write_operation.data = event[3]
            graphic_processor.set_operation(write_operation)
        elif action == Events.GENERATED_READ_OPERATION:
            graphic_processor = self.search_processor_by_id(event[1])
            read_operation = ReadOperation(event[1], logger=NoLogger())
            read_operation.address = event[2]
            graphic_processor.set_operation(read_operation)
        elif ( action == Events.REPLACING_BLOCK or action == Events.WRITING_BLOCK or 
              action == Events.UPDATING_BLOCK):
            graphic_processor = self.search_processor_by_id(event[1])
            new_cache_block = CacheBlock(event[2])
            new_cache_block.mem_address = event[3]
            new_cache_block.data = event[4]
            new_cache_block.state = event[5]
            graphic_processor.set_cache_block(event[2], new_cache_block)
        elif action == Events.WRITEBACK:
            address = event[2]
            data = event[3]
            self.graphic_memory.set_value(address, data)

    def update(self):
        while(self.eventQueue.is_empty() == False):
            next_event = self.eventQueue.get()
            self.handle_event(next_event)
            for processor in self.processors:
                processor.update()

        self.root.after(10, self.update)

    def __init__(self, eventQueue):
        self.root = tk.Tk()
        self.root.title("Loeclos Moesi")

        self.creating_processors()
        self.creating_memory()
        self.eventQueue = eventQueue

        self.update()

    def start(self):
        self.root.mainloop()
