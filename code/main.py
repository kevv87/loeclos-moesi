from threading import Thread

from code.processors.processors import Processor
from code.bus import Bus
from code.memory.memory import Memory

from code.ui.console import Console
from code.ui.graphic_tkinter.graphic_tkinter import GUI
from code.ui.event_queue import EventQueue

def start_gui(event_queue):
    gui = GUI(event_queue)

def start_model(event_queue):
    main_memory = Memory()
    main_bus = Bus(main_memory, logger=event_queue)

    alive_processors = []
    alive_processors.append(Processor(main_bus, logger=event_queue))
    alive_processors.append(Processor(main_bus, logger=event_queue))

    for processor in alive_processors:
        main_bus.subscribe(processor.cache)

    for processor in alive_processors:
        processor.start()

    for processor in alive_processors:
        processor.join()

def main():
    event_queue = EventQueue()

    model_thread = Thread(target=start_model, args=(event_queue,))
    model_thread.start()

    start_gui(event_queue)

    model_thread.join()

    print("Finished!")

main()
