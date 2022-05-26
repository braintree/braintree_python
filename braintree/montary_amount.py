from decimal import Decimal
from braintree.attribute_getter import AttributeGetter

class MontaryAmount(AttributeGetter):
    def __init__(self,attributes):
        AttributeGetter.__init__(self,attributes)
        if getattr(self, "value", None) is not None:
            self.value = Decimal(self.value)