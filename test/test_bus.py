import unittest
from unittest.mock import Mock, call

from code.bus import Bus
from code.operations import CalcOperation, WriteOperation, ReadOperation
from code.patterns.observer import SubscriberRsvp
from code.memory.memory import Memory

class BasicBus(unittest.TestCase):
    def setUp(self):
        self.memory_mock = Mock(spec = Memory())
        self.bus = Bus(self.memory_mock)
        self.subscriber = Mock(spec = SubscriberRsvp)
        self.subscriber.can_answer = True

        self.bus.subscribe(self.subscriber)

    def tearDown(self):
        self.bus.unsubscribeAll()

    def test_first_test(self):
        self.assertTrue(True)

    def test_bus_should_exist(self):
        self.assertTrue(Bus)

    def test_should_be_able_to_read_from_bus(self):
        operation = ReadOperation(1)
        operation_result = self.bus.read(operation)
        self.assertTrue(operation_result)

    def test_should_be_able_to_write_to_bus(self):
        operation = WriteOperation(1)
        operation_result = self.bus.write(operation)
        self.assertTrue(operation_result)

    def test_bus_should_have_a_semaphore(self):
        self.assertTrue(self.bus.semaphore)

    def test_bus_should_have_publisher_service(self):
        self.assertTrue(self.bus.publisher_service)

    def test_bus_should_notify_with_rsvp_subscribers_when_read(self):
        self.bus.read(ReadOperation(1))
        self.subscriber.notify_rsvp.assert_called()

    def test_bus_should_notify_subscribers_when_write(self):
        self.bus.write(WriteOperation(1))
        self.subscriber.notify.assert_called_once()
    
    def test_mem_operations_should_have_miss_attribute(self):
        operation = WriteOperation(1)
        self.assertFalse(operation.miss)

    def test_writeback_should_not_notify(self):
        operation = WriteOperation(1)

        self.bus.writeBack(operation)

        self.subscriber.notify.assert_not_called()

    def test_writeback_should_write_memory(self):
        operation = WriteOperation(1)

        self.bus.writeBack(operation)

        self.memory_mock.write_data.assert_called_once()

class BusNoShareableCopiesOnCaches(unittest.TestCase):
    def setUp(self):
        self.memory_mock = Mock(spec = Memory)
        self.memory_mock.read_data.return_value = 10
        self.memory_mock.write_data.return_value = True

        self.bus = Bus(self.memory_mock)
        for i in range(4):
            mock_cache = Mock(spec = SubscriberRsvp)
            mock_cache.notify_rsvp.return_value = False
            mock_cache.notify.return_value = True
            mock_cache.can_answer = True

            self.bus.subscribe(mock_cache)

    def tearDown(self):
        self.bus.unsubscribeAll()

    def test_bus_should_have_reference_to_memory(self):
        self.assertTrue(self.bus.memory)

    def test_bus_should_notify_two_times_to_search_owners_or_sharers(self):
        operation = ReadOperation(1)
        operation.miss = True
        self.bus.read(operation)
        for subscriber in self.bus.publisher_service.subscribers:
            subscriber.notify_rsvp.assert_called()
            self.assertEqual(subscriber.notify_rsvp.call_count, 2)
            subscriber.notify_rsvp.assert_has_calls(
                    [call(operation), 
                     call([False for subscriber in self.bus.publisher_service.subscribers])
                    ])
        
    def test_read_miss_should_retrieve_from_memory(self):
        operation = ReadOperation(1)
        operation.miss = True

        operation_result = self.bus.read(operation)

        self.assertEqual(operation_result, 10)
        self.memory_mock.read_data.assert_called()

    def test_read_hit_should_only_notify(self):
        operation = ReadOperation(1)
        operation.miss = False
        operation_result = self.bus.read(operation)

        for subscriber in self.bus.publisher_service.subscribers:
            subscriber.notify_rsvp.assert_called()

        self.memory_mock.read_data.assert_not_called()

    def test_write_should_only_notify(self):
        operation = WriteOperation(1)
        operation_result = self.bus.write(operation)

        for subscriber in self.bus.publisher_service.subscribers:
            subscriber.notify.assert_called()

        self.memory_mock.write_data.assert_not_called()

class BusShareableCopiesOnCaches(unittest.TestCase):
    def setUp(self):
        self.memory_mock = Mock(spec = Memory)
        self.memory_mock.read_data.return_value = 10

        self.bus = Bus(self.memory_mock)

        self.mock_cache_owner = Mock(spec = SubscriberRsvp)
        self.mock_cache_owner.notify_rsvp.return_value = 15

        self.mock_cache_owner.can_answer = True
        self.bus.subscribe(self.mock_cache_owner)

        for i in range(3):
            mock_cache = Mock(spec = SubscriberRsvp)
            mock_cache.notify_rsvp.side_effect = [False, 20]
            mock_cache.can_answer = True
            self.bus.subscribe(mock_cache)

    def tearDown(self):
        self.bus.unsubscribeAll()

    def test_read_miss_should_retrieve_from_cache_first_try(self):
        operation = ReadOperation(1)
        operation.miss = True

        operation_result = self.bus.read(operation)

        self.memory_mock.read_data.assert_not_called()

        for subscriber in self.bus.publisher_service.subscribers:
            subscriber.notify_rsvp.assert_called_with(operation)
            subscriber.notify.assert_called_with(operation_result)

        self.assertEqual(operation_result, 15)

    def test_read_miss_should_retrieve_from_cache_second_try(self):
        self.bus.publisher_service.unsubscribe(self.mock_cache_owner)

        operation = ReadOperation(1)
        operation.miss = True

        operation_result = self.bus.read(operation)

        self.memory_mock.read_data.assert_not_called()
        for subscriber in self.bus.publisher_service.subscribers:
            subscriber.notify_rsvp.assert_called()
            self.assertEqual(subscriber.notify_rsvp.call_count, 2)
            subscriber.notify_rsvp.assert_has_calls(
                    [call(operation), 
                     call([False for subscriber in self.bus.publisher_service.subscribers])
                    ])

        self.assertEqual(operation_result, 20)

    def test_read_hit_should_only_notify(self):
        operation = ReadOperation(1)
        operation.miss = False
        operation_result = self.bus.read(operation)

        for subscriber in self.bus.publisher_service.subscribers:
            subscriber.notify_rsvp.assert_called()

        self.memory_mock.read_data.assert_not_called()

    def test_write_should_only_notify(self):
        operation = WriteOperation(1)
        operation_result = self.bus.write(operation)

        for subscriber in self.bus.publisher_service.subscribers:
            subscriber.notify.assert_called()

        self.memory_mock.write_data.assert_not_called()

def test_bus_suite():
    print("### Starting test_bus_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicBus))
    suite.addTest(unittest.makeSuite(BusNoShareableCopiesOnCaches))
    suite.addTest(unittest.makeSuite(BusShareableCopiesOnCaches))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()

    runner.run(test_bus_suite())
