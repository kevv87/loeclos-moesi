import unittest
from unittest.mock import patch
import threading
import re
import time
import code.processors.processors as processors
from code.processors.constants import *
import code.my_random

class BasicProcessor(unittest.TestCase):
    def setUp(self):
        self.mock_bus = []
        self.processor = processors.Processor(self.mock_bus)

    def teardown(self):
        self.mock_bus = []

    def test_processor_file_should_exist(self):
        print("###test_processor_file_should_exist")
        self.assertTrue(processors)

    def test_should_exist_processor_class(self):
        print("###test_should_exist_processor_class")
        self.assertTrue(processors.Processor)

    def test_processor_should_have_number(self):
        print("###test_processor_should_have_number")
        self.assertTrue(self.processor.processor_number)

    def test_processor_numbers_should_be_unique(self):
        print("###test_processor_numbers_should_be_unique")
        p1 = processors.Processor(self.mock_bus)
        p2 = processors.Processor(self.mock_bus)
        self.assertNotEqual(p1.processor_number, p2.processor_number)

    def test_should_create_thread_when_instantiated(self):
        print("###test_should_create_thread_when_instantiated")
        p = processors.Processor(self.mock_bus)
        p.start()
        p.stop()
        p.join()
        self.assertIsInstance(p, threading.Thread)

    def test_create_calc_operation(self):
        print("###test_create_calc_operation")
        calcOperation = self.processor.create_calc_operation()
        self.assertTrue(calcOperation.operation_type == "calc")

    def test_create_write_operation(self):
        print("###test_create_write_operation")
        writeOperation = self.processor.create_write_operation()
        self.assertTrue(writeOperation.operation_type == "write")

    def test_create_read_operation(self):
        print("###test_create_read_operation")
        readOperation = self.processor.create_read_operation()
        self.assertTrue(readOperation.operation_type == "read")
    
    def test_processors_should_feed_a_bus(self):
        p1 = processors.Processor(self.mock_bus)
        p2 = processors.Processor(self.mock_bus)
        p1.start()
        p2.start()

        # Here processors are adding operations to the bus
        time.sleep(1)

        p1.stop()
        p2.stop()
        p1.join()
        p2.join()

        self.assertGreater(len(self.mock_bus), 0)
        for instruction in self.mock_bus:
            self.assertTrue(instruction.operation_type)
            self.assertTrue(instruction.processor_number)

    def test_processor_should_take_constant_time(self):
        print("###test_processor_should_take_constant_time")
        self.processor.start()

        time.sleep(PROCESSOR_ACTION_SECONDS * 3)
        
        self.processor.stop()
        self.processor.join()

        self.assertEqual(len(self.mock_bus), 3)

    def test_every_operation_type_should_have_common_fields(self):
        print("###test_every_operation_should_have_common_fields")
        calcOperation = self.processor.create_calc_operation()
        readOperation = self.processor.create_read_operation()
        writeOperation = self.processor.create_write_operation()

        self.assertTrue(calcOperation.operation_type)
        self.assertTrue(calcOperation.processor_number)

        self.assertTrue(readOperation.operation_type)
        self.assertTrue(readOperation.processor_number)

        self.assertTrue(writeOperation.operation_type)
        self.assertTrue(writeOperation.processor_number)

    def test_operations_should_have_their_generators_id(self):
        print("###test_operations_should_have_their_generators_id")
        calcOperation = self.processor.create_calc_operation()
        readOperation = self.processor.create_read_operation()
        writeOperation = self.processor.create_write_operation()

        self.assertTrue(calcOperation.processor_number == self.processor.processor_number)
        self.assertTrue(readOperation.processor_number == self.processor.processor_number)
        self.assertTrue(writeOperation.processor_number == self.processor.processor_number)

    def test_memory_operations_should_have_address(self):
        print("###test_memory_operations_should_have_fields")
        readOperation = self.processor.create_read_operation()
        writeOperation = self.processor.create_write_operation()

        self.assertTrue(readOperation.address)
        self.assertTrue(writeOperation.address)

    def test_address_should_be_binary(self):
        print("###test_address_should_be_binary")
        readOperation = self.processor.create_read_operation()
        writeOperation = self.processor.create_write_operation()

        binary_regexp = "^0b[0-1]+$"
        self.assertRegex(readOperation.get_address(), binary_regexp)
        self.assertRegex(writeOperation.get_address(), binary_regexp)

    def test_write_should_have_data(self):
        print("###test_write_should_have_data")
        writeOperation = self.processor.create_write_operation()
        self.assertTrue(writeOperation.data)

    def test_write_data_should_be_hex(self):
        print("###test_write_data_should_print_in_hex")
        writeOperation = self.processor.create_write_operation()

        hex_regexp = "^0x[0-9a-fA-F]+$"
        self.assertRegex(writeOperation.get_data(), hex_regexp)

def test_processors_suite():
    print("### Starting test_processors_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicProcessor))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()

    runner.run(test_processors_suite())
