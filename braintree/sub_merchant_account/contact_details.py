from braintree.attribute_getter import AttributeGetter
from braintree.sub_merchant_account.address_details import AddressDetails

class ContactDetails(AttributeGetter):
    detail_list = [
        "address_details",
        "date_of_birth",
        "email",
        "first_name",
        "last_name",
        "phone",
    ]

    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)
        self.address_details = AddressDetails(attributes.get("address", {}))

    def __repr__(self):
        return super(ContactDetails, self).__repr__(self.detail_list)
