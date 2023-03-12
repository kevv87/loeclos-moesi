import unittest
import code.processors as processors

class BasicProcessor(unittest.TestCase):
    def test_processor_file_should_exist(self):
        self.assertTrue(processors)

    def test_should_exist_processor_class(self):
        self.assertTrue(processors.Processor)

def test_processors_suite():
    print("### Starting test_processors_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicProcessor))
    return suite
