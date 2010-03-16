from braintree.util.http import Http
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.resource import Resource

class CreditCard(Resource):
    @staticmethod
    def create(params={}):
        Resource.verify_keys(params, CreditCard.__create_signature())
        response = Http().post("/payment_methods", {"credit_card": params})
        if "credit_card" in response:
            return SuccessfulResult({"credit_card": CreditCard(response["credit_card"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])
        else:
            pass

    @staticmethod
    def __create_signature():
        return ["customer_id", "cardholder_name", "cvv", "number", "expiration_date", "token"]

    def __init__(self, attributes):
        Resource.__init__(self, attributes)
        self.expiration_date = self.expiration_month + "/" + self.expiration_year

