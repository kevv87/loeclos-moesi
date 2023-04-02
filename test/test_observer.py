import unittest
from code.patterns.observer import (Publisher, Subscriber, PublisherRsvp,
                                    SubscriberRsvp)

class MockSubscriber():
    def __init__(self):
        self.notified = False

    def notify(self, msg=None):
        self.notified = True

class MockSubscriberRsvp():
    def __init__(self):
        self.notified = False
        self.can_answer = True

    def notify(self, msg=None):
        self.notified = True
        return "Hello World!"

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
        subscriber = MockSubscriber()
        self.publisher.subscribe(subscriber)
        self.publisher.notify_subscribers()
        self.assertTrue(subscriber.notified)

    def test_publisher_should_send_optional_msg(self):
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

class PublisherRsvpSuite(unittest.TestCase):
    def setUp(self):
        self.publisher = PublisherRsvp()
    
    def test_publisher_should_exist(self):
        self.assertTrue(self.publisher)

    def test_publisher_should_not_add_non_coherent_subscriber(self):
        with self.assertRaises(TypeError):
            self.publisher.subscribe(object())
            self.publisher.subscribe(MockSubscriber())

    def test_when_notifying_publisher_should_wait_response(self):
        subscriber = MockSubscriberRsvp()
        self.publisher.subscribe(subscriber)
        self.publisher.notify_subscribers_rsvp()
        self.assertTrue(subscriber.notified)
        self.assertEqual(self.publisher.subscribers_response,\
                         ["Hello World!"])

    def test_subscriber_should_accumulate_responses(self):
        class MockSubscriberRsvp():
            def __init__(self):
                self.notified = False
                self.can_answer = True

            def notify(self, msg=None):
                self.notified = True
                return "Hello World!"

        subscriber1 = MockSubscriberRsvp()
        subscriber2 = MockSubscriberRsvp()
        self.publisher.subscribe(subscriber1)
        self.publisher.subscribe(subscriber2)

        self.publisher.notify_subscribers_rsvp()

        self.assertEqual(len(self.publisher.subscribers_response),\
                            len(self.publisher.subscribers))
        self.assertEqual(self.publisher.subscribers_response,\
                         ["Hello World!", "Hello World!"])

def test_publisher_rsvp_suite():
    print("### Starting test_publisher_rsvp_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PublisherRsvpSuite))
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

class SuiteSubscriberRsvp(unittest.TestCase):
    def setUp(self):
        self.subscriber = SubscriberRsvp()

    def test_should_exist(self):
        self.assertTrue(self.subscriber)

    def test_should_announce_capability(self):
        self.assertTrue(self.subscriber.can_answer)

def test_subscriber_rsvp_suite():
    print("### Starting test_subscriber_rsvp_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SuiteSubscriberRsvp))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()

    #runner.run(test_publisher_suite())
    #runner.run(test_subscriber_suite())
    #runner.run(test_publisher_rsvp_suite())
    runner.run(test_subscriber_rsvp_suite())
