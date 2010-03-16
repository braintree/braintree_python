from braintree.util.http import Http
from braintree.successful_result import SuccessfulResult
from braintree.resource import Resource
from braintree.exceptions.argument_error import ArgumentError

class Customer(Resource):
    @staticmethod
    def create(params={}):
        Customer.__verify_keys(params, Customer.__create_signature())
        response = Http().post("/customers", {"customer": params})
        if "customer" in response:
            return SuccessfulResult({"customer": Customer(response["customer"])})
        else:
            pass

    @staticmethod
    def __create_signature():
        return ["company", "email", "fax", "first_name", "id", "last_name", "phone", "website"]

    @staticmethod
    def __verify_keys(params, signature):
        for key in params.keys():
            if not key in signature:
                raise ArgumentError(key + " is not an allowed key")
