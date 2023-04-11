from code.processors.processors import Processor
from code.bus import Bus
from code.memory.memory import Memory
from code.ui.console import Console

def main():
    logger = Console()

    main_memory = Memory()
    main_bus = Bus(main_memory, logger=logger)

    alive_processors = []
    alive_processors.append(Processor(main_bus, logger=logger))
    alive_processors.append(Processor(main_bus, logger=logger))

    for processor in alive_processors:
        main_bus.subscribe(processor.cache)

    for processor in alive_processors:
        processor.start()

    for processor in alive_processors:
        processor.join()

    print("Finished!")

main()
