from braintree.attribute_getter import AttributeGetter

class DirectorDetails(AttributeGetter):
    detail_list = [
        "first_name",
        "last_name",
        "email",
    ]

    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)

    def __repr__(self):
        return super(DirectorDetails, self).__repr__(self.detail_list)
