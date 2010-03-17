from braintree.attribute_getter import AttributeGetter

class SuccessfulResult(AttributeGetter):
    def __init__(self, attributes={}):
        self.is_success = True
        AttributeGetter.__init__(self, attributes)
