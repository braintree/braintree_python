from braintree.util.http import Http
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.resource import Resource
from braintree.credit_card import CreditCard
from braintree.exceptions.not_found_error import NotFoundError

class Customer(Resource):
    @staticmethod
    def create(params={}):
        Resource.verify_keys(params, Customer.create_signature())
        response = Http().post("/customers", {"customer": params})
        if "customer" in response:
            return SuccessfulResult({"customer": Customer(response["customer"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])
        else:
            pass

    @staticmethod
    def delete(customer_id):
        Http().delete("/customers/" + customer_id)
        return SuccessfulResult()

    @staticmethod
    def find(customer_id):
        try:
            response = Http().get("/customers/" + customer_id)
            return Customer(response["customer"])
        except NotFoundError:
            raise NotFoundError("customer with id " + customer_id + " not found")

    @staticmethod
    def update(customer_id, params={}):
        Resource.verify_keys(params, Customer.update_signature())
        response = Http().put("/customers/" + customer_id, {"customer": params})
        if "customer" in response:
            return SuccessfulResult({"customer": Customer(response["customer"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    @staticmethod
    def create_signature():
        return [
            "company", "email", "fax", "first_name", "id", "last_name", "phone", "website",
            {"credit_card": CreditCard.create_signature()},
            {"custom_fields": ["__any_key__"]}
        ]

    @staticmethod
    def update_signature():
        return [
            "company", "email", "fax", "first_name", "id", "last_name", "phone", "website",
            {"custom_fields": ["__any_key__"]}
        ]

    def __init__(self, attributes):
        Resource.__init__(self, attributes)
        if "credit_cards" in attributes:
            self.credit_cards = [CreditCard(credit_card) for credit_card in self.credit_cards]
