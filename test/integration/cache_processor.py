import unittest
from unittest.mock import Mock

from code.processors.processors import Processor
from code.bus import Bus

class BasicIntegration(unittest.TestCase):
    def test_processor_should_have_cache(self):
        mockBus = Mock(spec = Bus)
        processor = Processor(mockBus)
        self.assertTrue(processor.cache)

def processor_cache_suite():
    print("### Starting processor_cache_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicIntegration))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()

    runner.run(processor_cache_suite())

