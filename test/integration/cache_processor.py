import unittest
from unittest.mock import Mock

from code.processors.processors import Processor
from code.operations import ReadOperation
from code.bus import Bus
from code.memory.memory import Memory
from code.cache.moesi import Moesi
from code.cache.constants import *

from code.ui.console import Console

class BasicIntegration(unittest.TestCase):
    def test_error_stuck(self):
        main_memory = Memory()
        main_bus = Bus(main_memory, logger=Console())

        alive_processors = []
        alive_processors.append(Processor(main_bus, logger=Console()))
        alive_processors.append(Processor(main_bus, logger=Console()))

        for processor in alive_processors:
            main_bus.subscribe(processor.cache)

        alive_processors[0].cache.contents[0].state = MoesiStates.M
        alive_processors[0].cache.contents[0].address = 2
        alive_processors[0].cache.contents[0].data = 2

        readOperation = ReadOperation(alive_processors[1].processor_number)
        readOperation.address = 2
        result = alive_processors[1].cache.read(readOperation)
        self.assertEqual(result, 2)

def processor_cache_suite():
    print("### Starting processor_cache_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicIntegration))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()

    runner.run(processor_cache_suite())

