from braintree.attribute_getter import AttributeGetter
from braintree.monetary_amount import MonetaryAmount

class ExchangeRateQuote(AttributeGetter):
    def __init__(self,attributes):
        AttributeGetter.__init__(self,attributes)