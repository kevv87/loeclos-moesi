import unittest
from code.bus import Bus
from code.operations import CalcOperation, WriteOperation
from code.patterns.observer import Publisher

class BasicBus(unittest.TestCase):
    def setUp(self):
        self.bus = Bus()

    def test_first_test(self):
        self.assertTrue(True)

    def test_bus_should_exist(self):
        self.assertTrue(Bus)

    def test_bus_should_save_one_operation(self):
        operation = CalcOperation(1)
        self.bus.add_operation(operation)
        self.assertEqual(self.bus.current_operation, operation)

    def test_bus_should_pop_operations(self):
        operation = CalcOperation(1)
        self.bus.add_operation(operation)
        self.assertEqual(self.bus.pop_operation(), operation)
        self.assertEqual(self.bus.current_operation, None)

    def test_bus_should_have_a_semaphore(self):
        self.assertTrue(self.bus.semaphore)

    def test_adding_items_should_lower_semaphore(self):
        self.bus.add_operation(CalcOperation(1))
        self.assertEqual(self.bus.semaphore._value, 0)

    def test_popping_items_should_raise_semaphore(self):
        self.bus.add_operation(CalcOperation(1))
        self.assertEqual(self.bus.semaphore._value, 0)
        self.bus.pop_operation()
        self.assertEqual(self.bus.semaphore._value, 1)

    def test_bus_should_have_publisher_service(self):
        self.assertTrue(self.bus.publisher_service)

    def test_bus_should_notify_subscribers_when_added(self):
        class MockSubscriber():
            def __init__(self):
                self.notified = False

            def notify(self, msg = None):
                self.notified = True

        subscriber = MockSubscriber()
        self.bus.publisher_service.subscribe(subscriber)
        self.bus.add_operation(CalcOperation(1))
        self.assertTrue(subscriber.notified)
    
    def test_mem_operations_should_have_miss_attribute(self):
        operation = WriteOperation(1)
        self.assertFalse(operation.miss)

def test_bus_suite():
    print("### Starting test_bus_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicBus))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()

    runner.run(test_bus_suite())
