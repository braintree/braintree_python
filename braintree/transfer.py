from braintree.attribute_getter import AttributeGetter
from braintree.receiver import Receiver
from braintree.sender import Sender

class Transfer(AttributeGetter):
    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)
        if "sender" in attributes:
            self.sender = Sender(attributes["sender"])
        if "receiver" in attributes:
            self.receiver = Receiver(attributes["receiver"])
