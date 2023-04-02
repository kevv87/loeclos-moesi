import unittest
from code.patterns.observer import Publisher, Subscriber

class BasicPublisher(unittest.TestCase):
    def setUp(self):
        self.publisher = Publisher()

    def test_publisher_should_exist(self):
        self.assertTrue(Publisher)
    
    def test_publisher_should_have_a_list_of_subscribers(self):
        self.assertTrue(self.publisher.subscribers == [])

    def test_publisher_should_subscribe(self):
        subscriber = object()
        self.publisher.subscribe(subscriber)
        self.assertTrue(subscriber in self.publisher.subscribers)

    def test_publisher_should_unsubscribe(self):
        subscriber = object()
        self.publisher.subscribe(subscriber)
        self.assertTrue(subscriber in self.publisher.subscribers)
        self.publisher.unsubscribe(subscriber)
        self.assertFalse(subscriber in self.publisher.subscribers)

    def test_publisher_should_notify_subscribers(self):
        class MockSubscriber():
            def __init__(self):
                self.notified = False

            def notify(self, msg=None):
                self.notified = True

        subscriber = MockSubscriber()
        self.publisher.subscribe(subscriber)
        self.publisher.notify_subscribers()
        self.assertTrue(subscriber.notified)

    def test_publisher_should_send_optional_msg(self):
        class MockSubscriber():
            def __init__(self):
                self.notified = False
                self.msg = None

            def notify(self, msg=None):
                self.notified = True
                self.msg = msg

        subscriber = MockSubscriber()
        self.publisher.subscribe(subscriber)
        self.publisher.notify_subscribers("Hello World!")
        self.assertTrue(subscriber.notified)
        self.assertEqual(subscriber.msg, "Hello World!")

def test_publisher_suite():
    print("### Starting test_publisher_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicPublisher))
    return suite

class BasicSubscriber(unittest.TestCase):
    def setUp(self):
        self.subscriber = Subscriber()

    def test_subscriber_should_exist(self):
        self.assertTrue(self.subscriber)

    def test_subscriber_should_be_able_to_notify(self):
        self.assertTrue(self.subscriber.notify)

    def test_subscriber_should_receive_optional_msg(self):
        self.subscriber.notify("Hello World!")

def test_subscriber_suite():
    print("### Starting test_subscriber_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicSubscriber))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()

    runner.run(test_publisher_suite())
    runner.run(test_subscriber_suite())
