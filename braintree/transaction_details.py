from decimal import Decimal
from braintree.attribute_getter import AttributeGetter

class TransactionDetails(AttributeGetter):
    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)

        if self.amount is not None: #pylint: disable=E0203
            self.amount = Decimal(self.amount)
