from braintree.attribute_getter import AttributeGetter
from braintree.exceptions.argument_error import ArgumentError

class Resource(AttributeGetter):
    @staticmethod
    def verify_keys(params, signature):
        for key in params.keys():
            if not key in signature:
                raise ArgumentError(key + " is not an allowed key")
