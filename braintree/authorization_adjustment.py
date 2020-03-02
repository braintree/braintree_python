from decimal import Decimal
from braintree.attribute_getter import AttributeGetter

class AuthorizationAdjustment(AttributeGetter):
    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)
        if hasattr(self, 'amount') and self.amount is not None: #pylint: disable=E0203
            self.amount = Decimal(self.amount)
