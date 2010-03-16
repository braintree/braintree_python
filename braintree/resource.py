from braintree.attribute_getter import AttributeGetter

class Resource(AttributeGetter):
    @staticmethod
    def verify_keys(params, signature):
        for key in params.keys():
            if not key in signature:
                raise KeyError(key + " is not an allowed key")
