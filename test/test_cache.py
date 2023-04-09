import unittest
from code.cache.cache import Cache, CacheBlock
from code.cache.constants import *

from code.operations import WriteOperation, ReadOperation

class BasicCache(unittest.TestCase):
    def setUp(self):
        self.cache = Cache()

    def test_cache_should_exist(self):
        self.assertTrue(Cache)

    def test_cache_block_should_exist(self):
        self.assertTrue(CacheBlock)

    def test_cache_block_should_initialize_with_defaults(self):
        cache_block = CacheBlock(1)
        self.assertTrue(cache_block.number)

        self.assertEqual(cache_block.data, 0)
        self.assertEqual(cache_block.mem_address, 0)
        self.assertEqual(cache_block.state, MoesiStates.I)

    def notest_cache_block_should_have_basic_attributes(self):
        cache_block = CacheBlock(1)
        cache_block.data = 3
        cache_block.mem_address = 4
        cache_block.state = 1

        self.assertTrue(cache_block.number)
        self.assertTrue(cache_block.data)
        self.assertTrue(cache_block.mem_address)
        self.assertTrue(cache_block.state)

    def test_cache_should_have_four_blocks(self):
        cache = Cache()
        self.assertEqual(len(cache.contents), 4)

    def test_should_write_operation(self):
        write_operation = WriteOperation(2)

        expect_data = write_operation.data
        expect_address = write_operation.address
        self.cache.write(write_operation)

        found = False
        for block in self.cache.contents:
            if block.mem_address == write_operation.address:
                found = True
                break

        self.assertTrue(found)
        self.assertEqual(block.data, expect_data)
        self.assertEqual(block.mem_address, expect_address)

    def test_on_write_from_invalid_should_go_to_modified(self):
        write_operation = WriteOperation(2)
        self.cache.write(write_operation)

        found = False
        for block in self.cache.contents:
            if block.mem_address == write_operation.address:
                found = True
                break

        self.assertTrue(found)
        self.assertEqual(block.state, MoesiStates.M)

    def test_should_read_operation(self):
        write_operation = WriteOperation(2)
        self.cache.write(write_operation)

        read_operation = ReadOperation(2)
        read_operation.address = write_operation.address

        result_operation = self.cache.read(read_operation)

        self.assertEqual(result_operation, write_operation.data)

class AssociativityTests(unittest.TestCase):
    def setUp(self):
        self.cache = Cache()

    def test_odd_directions_should_go_on_zero_or_one(self):
        write_operation = WriteOperation(2)
        write_operation.address = 2
        self.cache.write(write_operation)

        block_zero = self.cache.contents[0]
        block_one = self.cache.contents[1]

        found = False

        if block_zero.mem_address == write_operation.address:
            found = True
        elif block_one.mem_address == write_operation.address:
            found = True

        self.assertTrue(found)

    def test_even_directions_should_go_on_two_or_three(self):
        write_operation = WriteOperation(2)
        write_operation.address = 3

        self.cache.write(write_operation)

        block_two = self.cache.contents[2]
        block_three = self.cache.contents[3]

        found = False

        if block_two.mem_address == write_operation.address:
            found = True
        elif block_three.mem_address == write_operation.address:
            found = True

        self.assertTrue(found)

    def test_should_prioritize_substitution_on_invalid_blocks(self):
        self.cache.contents[0].state = MoesiStates.M
        self.cache.contents[1].state = MoesiStates.I

        write_operation = WriteOperation(2)
        write_operation.address = 2

        self.cache.write(write_operation)

        invalid_block = self.cache.contents[1]

        self.assertEqual(invalid_block.mem_address, write_operation.address)

    def test_next_priority_are_shared_blocks(self):
        self.cache.contents[0].state = MoesiStates.S
        self.cache.contents[1].state = MoesiStates.O

        write_operation = WriteOperation(2)
        write_operation.address = 2

        self.cache.write(write_operation)

        shared_block = self.cache.contents[0]

        self.assertEqual(shared_block.mem_address, write_operation.address)

    def test_next_priority_are_exclusive_blocks(self):
        self.cache.contents[0].state = MoesiStates.O
        self.cache.contents[1].state = MoesiStates.E

        write_operation = WriteOperation(2)
        write_operation.address = 2

        self.cache.write(write_operation)

        exclusive_block = self.cache.contents[1]

        self.assertEqual(exclusive_block.mem_address, write_operation.address)

    def test_next_priority_are_modified_blocks(self):
        self.cache.contents[0].state = MoesiStates.M
        self.cache.contents[1].state = MoesiStates.O

        write_operation = WriteOperation(2)
        write_operation.address = 2

        self.cache.write(write_operation)

        modified_block = self.cache.contents[0]

        self.assertEqual(modified_block.mem_address, write_operation.address)

def test_cache_suite():
    print("### Starting test_cache_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicCache))
    suite.addTest(unittest.makeSuite(AssociativityTests))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(test_cache_suite())
