from braintree.attribute_getter import AttributeGetter
from braintree.montary_amount import MontaryAmount

class ExchangeRateQuote(AttributeGetter):
    def __init__(self,attributes):
        AttributeGetter.__init__(self,attributes)