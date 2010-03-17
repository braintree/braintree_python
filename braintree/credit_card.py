from braintree.util.http import Http
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.resource import Resource
from braintree.address import Address

class CreditCard(Resource):
    @staticmethod
    def create(params={}):
        Resource.verify_keys(params, CreditCard.create_signature())
        response = Http().post("/payment_methods", {"credit_card": params})
        if "credit_card" in response:
            return SuccessfulResult({"credit_card": CreditCard(response["credit_card"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])
        else:
            pass

    @staticmethod
    def create_signature():
        return [
            "customer_id", "cardholder_name", "cvv", "number", "expiration_date", "token",
            {"billing_address": Address.create_signature()},
            {"options": ["verify_card"]}
        ]

    def __init__(self, attributes):
        Resource.__init__(self, attributes)
        if "billing_address" in attributes:
            self.billing_address = Address(self.billing_address)
        self.expiration_date = self.expiration_month + "/" + self.expiration_year

