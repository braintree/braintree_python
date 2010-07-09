from braintree.attribute_getter import AttributeGetter

class CreditCardVerification(AttributeGetter):
    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)
        if "processor_response_code" not in attributes:
            self.processor_response_code = None
        if "processor_response_text" not in attributes:
            self.processor_response_text = None
