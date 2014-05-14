import braintree
from braintree.credit_card import CreditCard
from braintree.payment_method import PaymentMethod
from braintree.paypal_account import PayPalAccount
from braintree.error_result import ErrorResult
from braintree.exceptions.not_found_error import NotFoundError
from braintree.ids_search import IdsSearch
from braintree.resource import Resource
from braintree.resource_collection import ResourceCollection
from braintree.successful_result import SuccessfulResult

class PaymentMethodGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def create(self, params={}):
        Resource.verify_keys(params, PaymentMethod.create_signature())
        return self._post("/payment_methods", {"payment_method": params})

    def find(self, payment_method_token):
        try:
            if payment_method_token == None or payment_method_token.strip() == "":
                raise NotFoundError()

            response = self.config.http().get("/payment_methods/any/" + payment_method_token)
            if "paypal_account" in response:
                return PayPalAccount(self.gateway, response["paypal_account"])
            elif "credit_card" in response:
                return CreditCard(self.gateway, response["credit_card"]) 
        except NotFoundError:
            raise NotFoundError("payment method with token " + payment_method_token + " not found")


    def _post(self, url, params={}):
        response = self.config.http().post(url, params)
        if "paypal_account" in response:
            print response["paypal_account"]
            return SuccessfulResult({"payment_method": PayPalAccount(self.gateway, response["paypal_account"])})
        elif "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])

