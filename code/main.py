from code.processors.processors import Processor
from code.bus import Bus
from code.memory.memory import Memory

def main():
    main_memory = Memory()
    main_bus = Bus(main_memory)

    alive_processors = []
    alive_processors.append(Processor(main_bus))

    for processor in alive_processors:
        print("Starting processor {}".format(processor.processor_number))
        processor.start()

    for processor in alive_processors:
        processor.join()

    print("Finished!")


main()
