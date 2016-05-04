from braintree.attribute_getter import AttributeGetter
from braintree.sub_merchant_account.address_details import AddressDetails

class DirectorDetails(AttributeGetter):
    detail_list = [
        "first_name",
        "last_name",
        "email",
    ]

    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)
        self.address_details = AddressDetails(attributes.get("address", {}))

    def __repr__(self):
        return super(DirectorDetails, self).__repr__(self.detail_list)
