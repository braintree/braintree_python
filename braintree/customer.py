from braintree.util.http import Http
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.resource import Resource
from braintree.credit_card import CreditCard
from braintree.address import Address
from braintree.configuration import Configuration
from braintree.exceptions.not_found_error import NotFoundError
from braintree.transparent_redirect import TransparentRedirect

class Customer(Resource):
    @staticmethod
    def confirm_transparent_redirect(query_string):
        id = TransparentRedirect.parse_and_validate_query_string(query_string)
        return Customer.__post("/customers/all/confirm_transparent_redirect_request", {"id": id})

    @staticmethod
    def create(params={}):
        Resource.verify_keys(params, Customer.create_signature())
        return Customer.__post("/customers", {"customer": params})

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
    def tr_data_for_create(tr_data, redirect_url):
        Resource.verify_keys(tr_data, [{"customer": Customer.create_signature()}])
        return TransparentRedirect.tr_data(tr_data, redirect_url)

    @staticmethod
    def tr_data_for_update(tr_data, redirect_url):
        Resource.verify_keys(tr_data, [{"customer": Customer.update_signature()}])
        return TransparentRedirect.tr_data(tr_data, redirect_url)

    @staticmethod
    def transparent_redirect_create_url():
        return Configuration.base_merchant_url() + "/customers/all/create_via_transparent_redirect_request"

    @staticmethod
    def transparent_redirect_update_url():
        return Configuration.base_merchant_url() + "/customers/all/update_via_transparent_redirect_request"

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

    @staticmethod
    def __post(url, params={}):
        response = Http().post(url, params)
        if "customer" in response:
            return SuccessfulResult({"customer": Customer(response["customer"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])
        else:
            pass

    def __init__(self, attributes):
        Resource.__init__(self, attributes)
        if "credit_cards" in attributes:
            self.credit_cards = [CreditCard(credit_card) for credit_card in self.credit_cards]
        if "addresses" in attributes:
            self.addresses = [Address(address) for address in self.addresses]
