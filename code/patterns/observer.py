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

class Subscriber():
    def notify(self, msg=None):
        pass
