from braintree.attribute_getter import AttributeGetter

class FundingDetails(AttributeGetter):
    detail_list = [
        "account_holder_name",
        "bic",
        "currency_iso_code",
        "descriptor",
        "iban",
    ]

    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)

    def __repr__(self):
        return super(FundingDetails, self).__repr__(self.detail_list)
