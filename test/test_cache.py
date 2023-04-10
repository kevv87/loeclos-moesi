import unittest
from unittest.mock import Mock

from code.cache.cache import Cache, CacheBlock
from code.cache.moesi import Moesi
from code.cache.constants import *
from code.bus import Bus

from code.operations import WriteOperation, ReadOperation

class BasicCache(unittest.TestCase):
    def setUp(self):
        self.busMock = Mock(spec = Bus)
        self.cache = Cache(4, self.busMock)

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
        self.busMock = Mock(spec = Bus)
        cache = Cache(4, self.busMock)
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
        self.busMock = Mock(spec = Bus)
        self.cache = Cache(4, self.busMock)

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

class MoesiTests(unittest.TestCase):
    def test_moesi_should_exist(self):
        self.assertTrue(Moesi)

    def test_moesi_invalid_to_modified_on_self_write(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.I, MoesiEvents.SELF_WRITE)
        self.assertEqual(nextState, MoesiStates.M)

    def test_moesi_invalid_to_shared_on_self_non_exclusive_read(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.I, MoesiEvents.SELF_READ)
        self.assertEqual(nextState, MoesiStates.S)

    def test_moesi_invalid_to_exclusive_on_self_exclusive_read(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.I, MoesiEvents.EXCLUSIVE_READ)
        self.assertEqual(nextState, MoesiStates.E)

    def test_moesi_remains_invalid_on_other_operations(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.I, MoesiEvents.OTHERS_READ)
        self.assertEqual(nextState, MoesiStates.I)

        nextState = moesi.compute_next_state(MoesiStates.I, MoesiEvents.OTHERS_WRITE)
        self.assertEqual(nextState, MoesiStates.I)

    def test_moesi_modified_to_invalid_on_others_write(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.M, MoesiEvents.OTHERS_WRITE)
        self.assertEqual(nextState, MoesiStates.I)

    def test_moesi_modified_to_owner_on_others_read(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.M, MoesiEvents.OTHERS_READ)
        self.assertEqual(nextState, MoesiStates.O)

    def test_moesi_modified_remains_on_other_ops(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.M, MoesiEvents.SELF_WRITE)
        self.assertEqual(nextState, MoesiStates.M)

        nextState = moesi.compute_next_state(MoesiStates.M, MoesiEvents.SELF_READ)
        self.assertEqual(nextState, MoesiStates.M)

    def test_moesi_shared_to_invalid_on_others_write(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.S, MoesiEvents.OTHERS_WRITE)
        self.assertEqual(nextState, MoesiStates.I)

    def test_moesi_shared_to_modified_on_self_write(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.S, MoesiEvents.SELF_WRITE)
        self.assertEqual(nextState, MoesiStates.M)

    def test_moesi_shared_remains_on_other_ops(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.S, MoesiEvents.OTHERS_READ)
        self.assertEqual(nextState, MoesiStates.S)

        nextState = moesi.compute_next_state(MoesiStates.S, MoesiEvents.SELF_READ)
        self.assertEqual(nextState, MoesiStates.S)

    def test_moesi_exclusive_to_invalid_on_others_write(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.E, MoesiEvents.OTHERS_WRITE)
        self.assertEqual(nextState, MoesiStates.I)

    def test_moesi_exclusive_to_modified_on_self_write(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.E, MoesiEvents.SELF_WRITE)
        self.assertEqual(nextState, MoesiStates.M)

    def test_moesi_exclusive_to_shared_on_others_read(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.E, MoesiEvents.OTHERS_READ)
        self.assertEqual(nextState, MoesiStates.S)

    def test_moesi_exclusive_remains_on_other_ops(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.E, MoesiEvents.SELF_READ)
        self.assertEqual(nextState, MoesiStates.E)

    def test_moesi_owner_to_modified_on_self_write(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.O, MoesiEvents.SELF_WRITE)
        self.assertEqual(nextState, MoesiStates.M)

    def test_moesi_owner_to_invalid_on_others_write(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.O, MoesiEvents.OTHERS_WRITE)
        self.assertEqual(nextState, MoesiStates.I)

    def test_moesi_owner_remains_on_other_ops(self):
        moesi = Moesi()
        nextState = moesi.compute_next_state(MoesiStates.O, MoesiEvents.SELF_READ)
        self.assertEqual(nextState, MoesiStates.O)

        nextState = moesi.compute_next_state(MoesiStates.O, MoesiEvents.OTHERS_READ)
        self.assertEqual(nextState, MoesiStates.O)

class CacheStatesTests(unittest.TestCase):
    def setUp(self):
        self.busMock = Mock(spec = Bus)
        self.cache = Cache(4, self.busMock)
        self.cache.contents[0].address = 2
        self.cache.contents[1].address = 4
        self.cache.contents[2].address = 1
        self.cache.contents[3].address = 3

    def test_on_read_to_invalid_should_go_to_shared(self):
        self.cache.contents[0].state = MoesiStates.I
        readOperation = ReadOperation(2)
        readOperation.address = 2

        self.cache.read(readOperation)
        self.assertEqual(self.cache.contents[0].state, MoesiStates.S)

    def test_on_write_to_invalid_should_go_to_modified(self):
        self.cache.contents[0].state = MoesiStates.I
        writeOperation = WriteOperation(2)
        writeOperation.address = 2

        self.cache.write(writeOperation)
        self.assertEqual(self.cache.contents[0].state, MoesiStates.M)

    def test_exclusive_read_to_invalid_should_go_to_exclusive(self):
        self.cache.contents[0].state = MoesiStates.I
        readOperation = ReadOperation(2)
        readOperation.address = 10

        self.cache.read(readOperation)
        self.assertEqual(self.cache.contents[0].state, MoesiStates.E)

    def test_on_read_to_shared_should_remain_shared(self):
        self.cache.contents[0].state = MoesiStates.S
        readOperation = ReadOperation(2)
        readOperation.address = 2

        self.cache.read(readOperation)
        self.assertEqual(self.cache.contents[0].state, MoesiStates.S)

    def test_on_write_to_shared_should_go_to_modified(self):
        self.cache.contents[0].state = MoesiStates.S
        self.cache.contents[0].mem_address = 8

        writeOperation = WriteOperation(2)
        writeOperation.address = 8

        self.cache.write(writeOperation)
        self.assertEqual(self.cache.contents[0].state, MoesiStates.M)

    def test_on_notify_write_to_shared_should_go_to_invalid(self):
        self.cache.contents[0].state = MoesiStates.S
        self.cache.contents[0].mem_address = 8

        writeOperation = WriteOperation(2)
        writeOperation.address = 8

        self.cache.notify(writeOperation)
        self.assertEqual(self.cache.contents[0].state, MoesiStates.I)

    def test_on_notify_read_to_shared_should_remain_shared(self):
        self.cache.contents[0].state = MoesiStates.S
        self.cache.contents[0].mem_address = 8

        readOperation = ReadOperation(2)
        readOperation.address = 8

        self.cache.notify(readOperation)
        self.assertEqual(self.cache.contents[0].state, MoesiStates.S)

    def test_read_to_exclusive_should_remain_exclusive(self):
        self.cache.contents[0].state = MoesiStates.E
        self.cache.contents[0].mem_address = 8

        readOperation = ReadOperation(2)
        readOperation.address = 8

        self.cache.read(readOperation)

        self.assertEqual(self.cache.contents[0].state, MoesiStates.E)

    def test_write_to_exclusive_should_go_to_modified(self):
        self.cache.contents[0].state = MoesiStates.E
        self.cache.contents[0].mem_address = 8

        writeOperation = WriteOperation(2)
        writeOperation.address = 8

        self.cache.write(writeOperation)

        self.assertEqual(self.cache.contents[0].state, MoesiStates.M)

    def test_on_notify_read_to_exclusive_should_go_to_shared(self):
        self.cache.contents[0].state = MoesiStates.E
        self.cache.contents[0].mem_address = 8

        readOperation = ReadOperation(2)
        readOperation.address = 8

        self.cache.notify(readOperation)

        self.assertEqual(self.cache.contents[0].state, MoesiStates.S)

    def test_on_notify_write_to_exclusive_should_go_to_invalid(self):
        self.cache.contents[0].state = MoesiStates.E
        self.cache.contents[0].mem_address = 8

        writeOperation = WriteOperation(2)
        writeOperation.address = 8

        self.cache.notify(writeOperation)

        self.assertEqual(self.cache.contents[0].state, MoesiStates.I)

    def test_read_to_owner_should_remain_owner(self):
        self.cache.contents[0].state = MoesiStates.O
        self.cache.contents[0].mem_address = 8

        readOperation = ReadOperation(2)
        readOperation.address = 8

        self.cache.read(readOperation)

        self.assertEqual(self.cache.contents[0].state, MoesiStates.O)

    def test_write_to_owner_should_go_to_modified(self):
        self.cache.contents[0].state = MoesiStates.O
        self.cache.contents[0].mem_address = 8

        writeOperation = WriteOperation(2)
        writeOperation.address = 8

        self.cache.write(writeOperation)

        self.assertEqual(self.cache.contents[0].state, MoesiStates.M)

    def test_on_notify_read_to_owner_should_remain_owner(self):
        self.cache.contents[0].state = MoesiStates.O
        self.cache.contents[0].mem_address = 8

        readOperation = ReadOperation(2)
        readOperation.address = 8

        self.cache.notify(readOperation)

        self.assertEqual(self.cache.contents[0].state, MoesiStates.O)

    def test_on_notify_write_to_owner_should_go_to_invalid(self):
        self.cache.contents[0].state = MoesiStates.O
        self.cache.contents[0].mem_address = 8

        writeOperation = WriteOperation(2)
        writeOperation.address = 8

        self.cache.notify(writeOperation)

        self.assertEqual(self.cache.contents[0].state, MoesiStates.I)

    def test_read_to_modified_should_remain_modified(self):
        self.cache.contents[0].state = MoesiStates.M
        self.cache.contents[0].mem_address = 8

        readOperation = ReadOperation(2)
        readOperation.address = 8

        self.cache.read(readOperation)

        self.assertEqual(self.cache.contents[0].state, MoesiStates.M)

    def test_write_to_modified_should_remain_modified(self):
        self.cache.contents[0].state = MoesiStates.M
        self.cache.contents[0].mem_address = 8

        writeOperation = WriteOperation(2)
        writeOperation.address = 8

        self.cache.write(writeOperation)

        self.assertEqual(self.cache.contents[0].state, MoesiStates.M)

    def test_on_notify_write_to_modified_should_go_to_invalid(self):
        self.cache.contents[0].state = MoesiStates.M
        self.cache.contents[0].mem_address = 8

        writeOperation = WriteOperation(2)
        writeOperation.address = 8

        self.cache.notify(writeOperation)

        self.assertEqual(self.cache.contents[0].state, MoesiStates.I)

    def test_on_notify_read_to_modified_should_go_to_owner(self):
        self.cache.contents[0].state = MoesiStates.M
        self.cache.contents[0].mem_address = 8

        readOperation = ReadOperation(2)
        readOperation.address = 8

        self.cache.notify(readOperation)

        self.assertEqual(self.cache.contents[0].state, MoesiStates.O)

    def test_cache_should_ignore_own_notifications(self):
        self.cache.contents[0].state = MoesiStates.M
        self.cache.contents[0].mem_address = 8

        writeOperation = WriteOperation(4)
        writeOperation.address = 8

        self.cache.notify(writeOperation)

        self.assertEqual(self.cache.contents[0].state, MoesiStates.M)

class CacheResponsesTests(unittest.TestCase):
    def setUp(self):
        self.busMock = Mock(spec = Bus)
        self.cache = Cache(4, self.busMock)

    def test_cache_should_have_reference_to_bus(self):
        self.assertEqual(self.cache.bus, self.busMock)

    def test_cache_when_block_moves_from_modified_to_invalid_should_writeback(self):
        self.cache.contents[0].state = MoesiStates.M
        self.cache.contents[0].mem_address = 8

        writeOperation = WriteOperation(2)
        writeOperation.address = 8

        self.cache.notify(writeOperation)

        self.busMock.writeBack.assert_called_once_with(writeOperation)

    def test_cache_when_block_moves_from_owner_to_invalid_should_writeback(self):
        self.cache.contents[0].state = MoesiStates.O
        self.cache.contents[0].mem_address = 8

        writeOperation = WriteOperation(2)
        writeOperation.address = 8

        self.cache.notify(writeOperation)

        self.busMock.writeBack.assert_called_once_with(writeOperation)

    #TODO: Hay que verificar si las notificaciones son propias o de otro procesador

def test_cache_suite():
    print("### Starting test_cache_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicCache))
    suite.addTest(unittest.makeSuite(AssociativityTests))
    suite.addTest(unittest.makeSuite(MoesiTests))
    suite.addTest(unittest.makeSuite(CacheStatesTests))
    suite.addTest(unittest.makeSuite(CacheResponsesTests))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(test_cache_suite())
