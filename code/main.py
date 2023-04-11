import tkinter as tk
import tkinter.simpledialog as sd

from threading import Thread, Event

from code.processors.processors import Processor
from code.bus import Bus
from code.memory.memory import Memory
from code.operations import CalcOperation, WriteOperation, ReadOperation

from code.ui.console import Console, NoLogger
from code.ui.graphic_tkinter.graphic_tkinter import GUI
from code.ui.event_queue import EventQueue

pause_event = Event()
step_event = Event()

event_queue = EventQueue()
gui = GUI(event_queue)

p1_queue = []
p2_queue = []
p3_queue = []
p4_queue = []

alive_processors = []

def pressed_pause():
    event_queue.clear()
    if pause_event.is_set():
        pause_event.clear()
    else:
        pause_event.set()

def process_text_command(text_command):
    text_command_splitted = text_command.split(" ")
    operation = text_command_splitted[0]
    if operation == "write":
        address = text_command_splitted[2]
        data = text_command_splitted[1]
        writeOperation = WriteOperation(0, logger=NoLogger())
        writeOperation.address = int(address, 0)
        writeOperation.data = int(data, 0)
        return writeOperation
    elif operation == "read":
        address = text_command_splitted[1]
        readOperation = ReadOperation(0, logger=NoLogger())
        readOperation.address = int(address, 0)
        return readOperation
    elif operation == "calc":
        return CalcOperation(0, logger=NoLogger())

def pressed_p1():
    text_command = sd.askstring("Input", "Enter the next instruction for P1:")
    operation = process_text_command(text_command)
    if not operation:
        return pressed_p1()
    else:
        operation.processor_number = gui.processors[0].number
        print("New operation in p1 queue")
        p1_queue.append(operation)

def pressed_p2():
    text_command = sd.askstring("Input", "Enter the next instruction for P2:")
    operation = process_text_command(text_command)
    if not operation:
        return pressed_p2()
    else:
        operation.processor_number = gui.processors[1].number
        print("New operation in p2 queue")
        p2_queue.append(operation)

def pressed_p3():
    text_command = sd.askstring("Input", "Enter the next instruction for P3:")
    operation = process_text_command(text_command)
    if not operation:
        return pressed_p3()
    else:
        operation.processor_number = gui.processors[2].number
        print("New operation in p3 queue")
        p3_queue.append(operation)

def pressed_p4():
    text_command = sd.askstring("Input", "Enter the next instruction for P4:")
    operation = process_text_command(text_command)
    if not operation:
        return pressed_p4()
    else:
        operation.processor_number = gui.processors[3].number
        print("New operation in p4 queue")
        p4_queue.append(operation)

def pressed_step():
    event_queue.clear()
    for processor in alive_processors:
        processor.do_step()

def start_gui(event_queue):
    root = gui.root

    pause_button = tk.Button(root, text="Pause", command=pressed_pause)
    pause_button.pack()

    step_button = tk.Button(root, text="Step", command=pressed_step)
    step_button.pack()

    p1_button = tk.Button(root, text="P1", command=pressed_p1)
    p1_button.pack()

    p2_button = tk.Button(root, text="P2", command=pressed_p2)
    p2_button.pack()

    p3_button = tk.Button(root, text="P3", command=pressed_p3)
    p3_button.pack()

    p4_button = tk.Button(root, text="P4", command=pressed_p4)
    p4_button.pack()

    gui.start()

def start_model(event_queue):
    main_memory = Memory()
    main_bus = Bus(main_memory, logger=event_queue)


    alive_processors.append(Processor(main_bus, pause_event, p1_queue, logger=event_queue))
    alive_processors.append(Processor(main_bus, pause_event, p2_queue, logger=event_queue))
    alive_processors.append(Processor(main_bus, pause_event, p3_queue, logger=event_queue))
    alive_processors.append(Processor(main_bus, pause_event, p4_queue, logger=event_queue))

    for processor in alive_processors:
        main_bus.subscribe(processor.cache)

    for processor in alive_processors:
        processor.start()

    for processor in alive_processors:
        processor.join()

def main():

    model_thread = Thread(target=start_model, args=(event_queue,))
    model_thread.start()

    start_gui(event_queue)

    model_thread.join()

    print("Finished!")

main()
