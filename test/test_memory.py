import unittest

from code.memory.constants import *
from code.processors.constants import *

from code.memory.memory import Memory
from code.memory.error_types import SegmentationFault, DataOverflow
import time

class BasicMemory(unittest.TestCase):
    def setUp(self):
        self.memory_instance = Memory()

    def test_first_test(self):
        self.assertTrue(True)

    def test_memory_should_exist(self):
        self.assertIsNotNone(Memory)

    def test_memory_should_have_a_store_array(self):
        self.assertIsNotNone(self.memory_instance.contents)

    def test_memory_store_array_should_be_of_constant_length(self):
        self.assertEqual(len(self.memory_instance.contents), MEMORY_BLOCK_WIDTH)

    def test_memory_should_be_0_initially(self):
        for i in range(0, MEMORY_BLOCK_WIDTH):
            self.assertEqual(self.memory_instance.contents[i], 0)

class MemoryWriting(unittest.TestCase):
    def setUp(self):
        self.memory_instance = Memory()

    def test_should_write_data_to_memory(self):
        self.memory_instance.write_data(0, 1, real_time=False)
        self.assertEqual(self.memory_instance.contents[0], 1)

    def test_write_data_should_fail_if_address_is_out_of_bounds(self):
        with self.assertRaises(SegmentationFault):
            self.memory_instance.write_data(MEMORY_BLOCK_WIDTH, 1, real_time=False)

        with self.assertRaises(SegmentationFault):
            self.memory_instance.write_data(MEMORY_BLOCK_WIDTH, -1, real_time=False)

    def test_write_data_should_fail_if_data_is_out_of_bounds(self):
        max_val = (1 << MEMORY_BLOCK_DEPTH_BITS - 1) - 1
        min_val = -max_val - 1

        with self.assertRaises(DataOverflow):
            self.memory_instance.write_data(0, max_val + 1, real_time=False)

        with self.assertRaises(DataOverflow):
            self.memory_instance.write_data(0, min_val - 1, real_time=False)

    def test_write_data_edge_cases_should_be_ok(self):
        max_val = (1 << MEMORY_BLOCK_DEPTH_BITS - 1) - 1
        min_val = -max_val - 1

        self.memory_instance.write_data(0, max_val, real_time=False)
        self.assertEqual(self.memory_instance.contents[0], max_val)

        self.memory_instance.write_data(0, min_val, real_time=False)
        self.assertEqual(self.memory_instance.contents[0], min_val)

    def test_writing_data_should_take_triple_time_than_processor_action(self):
        start_timer = time.time()

        self.memory_instance.write_data(0, 1)
        self.assertEqual(self.memory_instance.contents[0], 1)

        elapsed_time = time.time() - start_timer
        time_taken_by_processor = PROCESSOR_ACTION_SECONDS
        
        self.assertGreaterEqual(elapsed_time, time_taken_by_processor * 3)

class MemoryReading(unittest.TestCase):
    def setUp(self):
        self.memory_instance = Memory()
        self.memory_instance.contents = [x for x in range(0, MEMORY_BLOCK_WIDTH)]

    def test_should_read_data(self):
        value = self.memory_instance.read_data(0, real_time=False)
        self.assertEqual(value, 0)

    def test_should_read_expected_data(self):
        for i in range(0, MEMORY_BLOCK_WIDTH):
            value = self.memory_instance.read_data(i, real_time=False)
            self.assertEqual(value, i)

    def test_reading_data_should_take_triple_time_than_processor_action(self):
        start_timer = time.time()

        self.memory_instance.read_data(0)

        elapsed_time = time.time() - start_timer
        time_taken_by_processor = PROCESSOR_ACTION_SECONDS
        
        self.assertGreaterEqual(elapsed_time, time_taken_by_processor * 3)

    def test_read_data_should_fail_if_address_is_out_of_bounds(self):
        with self.assertRaises(SegmentationFault):
            self.memory_instance.read_data(MEMORY_BLOCK_WIDTH, real_time=False)

        with self.assertRaises(SegmentationFault):
            self.memory_instance.read_data(MEMORY_BLOCK_WIDTH, real_time=False)

class VisualizeMemory(unittest.TestCase):
    def setUp(self):
        self.memory_instance = Memory()
        self.memory_instance.contents = [x for x in range(0, MEMORY_BLOCK_WIDTH)]

    def test_memory_should_be_visualized(self):
        memory_state = self.memory_instance.visualize()
        self.assertEqual(memory_state, self.memory_instance.contents)

def test_memory_suite():
    print("### Starting test_memory_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicMemory))
    suite.addTest(unittest.makeSuite(MemoryWriting))
    suite.addTest(unittest.makeSuite(MemoryReading))
    suite.addTest(unittest.makeSuite(VisualizeMemory))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()

    runner.run(test_memory_suite())
