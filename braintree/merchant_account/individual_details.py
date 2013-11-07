from braintree.attribute_getter import AttributeGetter

class IndividualDetails(AttributeGetter):
    class AddressDetails(AttributeGetter):
        detail_list = [
            "street_address",
            "locality",
            "region",
            "postal_code",
        ]

        def __init__(self, attributes):
            AttributeGetter.__init__(self, attributes)

        def __repr__(self):
            return super(IndividualDetails.AddressDetails, self).__repr__(self.detail_list)

    detail_list = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "date_of_birth",
        "ssn_last_4",
        "address_details",
    ]

    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)
        self.address = IndividualDetails.AddressDetails(attributes.get("address_details", {}))

    def __repr__(self):
        return super(IndividualDetails, self).__repr__(self.detail_list)
