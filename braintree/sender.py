from braintree.attribute_getter import AttributeGetter

class Sender(AttributeGetter):
    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)
