import urlparse
from braintree.util.http import Http
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.resource import Resource
from braintree.address import Address
from braintree.exceptions.not_found_error import NotFoundError
from braintree.configuration import Configuration
from braintree.transparent_redirect import TransparentRedirect

class CreditCard(Resource):
    @staticmethod
    def confirm_transparent_redirect(query_string):
        id = urlparse.parse_qs(query_string)["id"][0]
        return CreditCard.__post("/payment_methods/all/confirm_transparent_redirect_request", {"id": id})

    @staticmethod
    def create(params={}):
        Resource.verify_keys(params, CreditCard.create_signature())
        return CreditCard.__post("/payment_methods", {"credit_card": params})

    @staticmethod
    def update(credit_card_token, params={}):
        Resource.verify_keys(params, CreditCard.update_signature())
        response = Http().put("/payment_methods/" + credit_card_token, {"credit_card": params})
        if "credit_card" in response:
            return SuccessfulResult({"credit_card": CreditCard(response["credit_card"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    @staticmethod
    def delete(credit_card_token):
        Http().delete("/payment_methods/" + credit_card_token)
        return SuccessfulResult()

    @staticmethod
    def find(credit_card_token):
        try:
            response = Http().get("/payment_methods/" + credit_card_token)
            return CreditCard(response["credit_card"])
        except NotFoundError:
            raise NotFoundError("payment method with token " + credit_card_token + " not found")

    @staticmethod
    def create_signature():
        return [
            "customer_id", "cardholder_name", "cvv", "number", "expiration_date", "expiration_month",
            "expiration_year", "token",
            {"billing_address": Address.create_signature()},
            {"options": ["verify_card"]}
        ]

    @staticmethod
    def update_signature():
        return [
            "cardholder_name", "cvv", "number", "expiration_date", "expiration_month", "expiration_year", "token",
            {"options": ["verify_card"]},
            {"billing_address":
                [
                    "first_name", "last_name", "company", "country_name", "extended_address", "locality", "region",
                    "postal_code", "street_address"
                ]
            }
        ]

    @staticmethod
    def transparent_redirect_create_url():
        return Configuration.base_merchant_url() + "/payment_methods/all/create_via_transparent_redirect_request"

    @staticmethod
    def tr_data_for_create(tr_data, redirect_url):
        Resource.verify_keys(tr_data, [{"credit_card": CreditCard.create_signature()}])
        return TransparentRedirect.tr_data(tr_data, redirect_url)

    @staticmethod
    def tr_data_for_update(tr_data, redirect_url):
        Resource.verify_keys(tr_data, ["payment_method_token", {"credit_card": CreditCard.create_signature()}])
        return TransparentRedirect.tr_data(tr_data, redirect_url)

    @staticmethod
    def transparent_redirect_update_url():
        return Configuration.base_merchant_url() + "/payment_methods/all/update_via_transparent_redirect_request"

    @staticmethod
    def __post(url, params):
        response = Http().post(url, params)
        if "credit_card" in response:
            return SuccessfulResult({"credit_card": CreditCard(response["credit_card"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    def __init__(self, attributes):
        Resource.__init__(self, attributes)
        if "billing_address" in attributes:
            self.billing_address = Address(self.billing_address)

    @property
    def expiration_date(self):
        return self.expiration_month + "/" + self.expiration_year

    @property
    def masked_number(self):
        return self.bin + "******" + self.last_4

