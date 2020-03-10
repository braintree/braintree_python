from decimal import Decimal
from braintree.attribute_getter import AttributeGetter

class AuthorizationAdjustment(AttributeGetter):
    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)
        if getattr(self, "amount", None) is not None:
            self.amount = Decimal(self.amount)
