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

class PublisherRsvp(Publisher):
    def subscribe(self, subscriber):
        if not hasattr(subscriber, 'can_answer') or\
                not subscriber.can_answer:
            raise TypeError("Subscriber cannot answer rsvps")

        super().subscribe(subscriber)

    def notify_subscribers_rsvp(self, msg=None):
        subscribers_response = []
        for subscriber in self.subscribers:
            subscribers_response.append(subscriber.notify_rsvp(msg))
        return subscribers_response
    
    def unsubscribeAll(self):
        self.subscribers = []

class Subscriber():
    def notify(self, msg=None):
        pass

class SubscriberRsvp(Subscriber):
    def __init__(self):
        self.can_answer = True

    def notify_rsvp(self, msg=None):
        return None
