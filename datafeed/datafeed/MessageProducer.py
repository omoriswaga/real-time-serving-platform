"""MessageProducer is the base class to be used when creating a more specific
message bus producer implementation.
"""
class MessageProducer:
    def send(self, _: dict):
        pass
