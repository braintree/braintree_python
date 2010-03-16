from braintree.util.http import Http
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.resource import Resource
from braintree.credit_card import CreditCard

class Customer(Resource):
    @staticmethod
    def create(params={}):
        Resource.verify_keys(params, Customer.__create_signature())
        response = Http().post("/customers", {"customer": params})
        if "customer" in response:
            return SuccessfulResult({"customer": Customer(response["customer"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])
        else:
            pass

    @staticmethod
    def __create_signature():
        return ["company", "credit_card", "email", "fax", "first_name", "id", "last_name", "phone", "website"]

    def __init__(self, attributes):
        Resource.__init__(self, attributes)
        self.credit_cards = [CreditCard(credit_card) for credit_card in self.credit_cards]
