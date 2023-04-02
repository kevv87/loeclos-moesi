from threading import Thread

class Publisher():
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def notify_subscribers(self, msg=None):
        for subscriber in self.subscribers:
            subscriber.notify(msg)

    def unsubscribeAll(self):
        self.subscribers = []

class PublisherRsvp(Publisher):
    def subscribe(self, subscriber):
        if not hasattr(subscriber, 'can_answer') or\
                not subscriber.can_answer:
            raise TypeError("Subscriber cannot answer rsvps")

        super().subscribe(subscriber)

    def notify_subscribers_rsvp(self, msg=None):
        result = None
        wait_threads = []
        threads_results = []
        for subscriber in self.subscribers:
            thread = Thread(target=self.wait_for_response,
                       args=(subscriber, threads_results) )
            wait_threads.append(thread)
            thread.start()

        for thread in wait_threads:
            thread.join()

        return threads_results

    def wait_for_response(self, subscriber, threads_results):
        threads_results.append(subscriber.notify_rsvp())

class Subscriber():
    def notify(self, msg=None):
        pass

class SubscriberRsvp(Subscriber):
    def __init__(self):
        self.can_answer = True

    def notify_rsvp(self, msg=None):
        return None
