from braintree.attribute_getter import AttributeGetter

class BusinessDetails(AttributeGetter):
    detail_list = [
        "dba_name",
        "tax_id",
    ]

    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)

    def __repr__(self):
        return super(BusinessDetails, self).__repr__(self.detail_list)
