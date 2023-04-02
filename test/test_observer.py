import unittest
from code.patterns.observer import (Publisher, Subscriber, PublisherRsvp,
                                    SubscriberRsvp)
from unittest.mock import patch, Mock, MagicMock, call, ANY

class MockSubscriber():
    def __init__(self):
        self.notified = False

    def notify(self, msg=None):
        self.notified = True

class MockSubscriberRsvp():
    def __init__(self):
        self.notified = False
        self.can_answer = True

    def notify_rsvp(self, msg=None):
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

def test_publisher_suite():
    print("### Starting test_publisher_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicPublisher))
    return suite

class PublisherRsvpSuite(unittest.TestCase):
    def setUp(self):
        self.publisher = PublisherRsvp()

    def tearDown(self):
        self.publisher.unsubscribeAll()
    
    def test_publisher_should_exist(self):
        self.assertTrue(self.publisher)

    def test_publisher_should_not_add_non_coherent_subscriber(self):
        with self.assertRaises(TypeError):
            self.publisher.subscribe(object())
            self.publisher.subscribe(MockSubscriber())

    def test_when_notifying_publisher_should_wait_response(self):
        subscriber = MockSubscriberRsvp()
        self.publisher.subscribe(subscriber)
        response = self.publisher.notify_subscribers_rsvp()
        self.assertTrue(subscriber.notified)
        self.assertEqual(response,\
                         ["Hello World!"])

    def test_publisher_should_create_threads_to_listen(self):
        # Create a MagicMock object to mock the wait_for_response method
        wait_for_response_mock = MagicMock()

        # Patch the wait_for_response method with the MagicMock object
        with patch.object(PublisherRsvp, 'wait_for_response', wait_for_response_mock):
            patched_publisher = PublisherRsvp()
            for i in range(3):
                mock_subscriber = Mock(spec=SubscriberRsvp)
                mock_subscriber.can_answer = True
                patched_publisher.subscribe(mock_subscriber)

            patched_publisher.notify_subscribers_rsvp()

            # Assert that the wait_for_response method was called three times
            self.assertEqual(wait_for_response_mock.call_count, 3)

            # Assert that each call to wait_for_response was passed a subscriber and a list to store the thread's results
            wait_for_response_mock.assert_has_calls(
                [call(subscriber, ANY) for subscriber in patched_publisher.subscribers],
                any_order=True
            )

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

    runner.run(test_publisher_suite())
    runner.run(test_subscriber_suite())
    runner.run(test_publisher_rsvp_suite())
    runner.run(test_subscriber_rsvp_suite())
