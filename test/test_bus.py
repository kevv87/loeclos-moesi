import unittest
from code.bus import Bus
from code.operations import CalcOperation, WriteOperation, ReadOperation
from code.patterns.observer import SubscriberRsvp

class BasicBus(unittest.TestCase):
    class MockSubscriberRsvp():
        def __init__(self):
            self.notified = False
            self.can_answer = True
        def notify_rsvp(self, msg = None):
            self.notified = True
            return True
        def notify(self, msg = None):
            self.notified = True

    def setUp(self):
        self.bus = Bus()
        self.subscriber = self.MockSubscriberRsvp()
        self.bus.subscribe(self.subscriber)

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
        self.assertTrue(self.subscriber.notified)

    def test_bus_should_notify_subscribers_when_write(self):
        self.bus.write(WriteOperation(1))
        self.assertTrue(self.subscriber.notified)
    
    def test_mem_operations_should_have_miss_attribute(self):
        operation = WriteOperation(1)
        self.assertFalse(operation.miss)

class BusNoShareableCopiesOnCaches(unittest.TestCase):
    class MockCacheWithNoShareableCopy(SubscriberRsvp):
        def __init__(self):
            pass

        def notify(self, msg = None):
            pass

        def notify_rsvp(self, msg=None):
            return False

    def setUp(self):
        self.bus = Bus()
        subscribers = []
        for i in range(4):
            subscribers.append(MockCacheWithNoShareableCopy())

def test_bus_suite():
    print("### Starting test_bus_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicBus))
    #suite.addTest(unittest.makeSuite(BusNoShareableCopiesOnCaches))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()

    runner.run(test_bus_suite())
