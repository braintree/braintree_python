from braintree.attribute_getter import AttributeGetter
from braintree.sub_merchant import SubMerchant

class PaymentFacilitator(AttributeGetter):
    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)
        if "sub_merchant" in attributes:
            self.sub_merchant = SubMerchant(attributes["sub_merchant"])
