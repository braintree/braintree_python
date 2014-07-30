import braintree
from braintree.credit_card import CreditCard
from braintree.payment_method import PaymentMethod
from braintree.paypal_account import PayPalAccount
from braintree.sepa_bank_account import SEPABankAccount
from braintree.unknown_payment_method import UnknownPaymentMethod
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
            return self._parse_payment_method(response)
        except NotFoundError:
            raise NotFoundError("payment method with token " + payment_method_token + " not found")

    def update(self, payment_method_token, params):
        Resource.verify_keys(params, PaymentMethod.update_signature())
        try:
            if payment_method_token == None or payment_method_token.strip() == "":
                raise NotFoundError()

            return self._put(
                "/payment_methods/any/" + payment_method_token,
                {"payment_method": params}
            )
        except NotFoundError:
            raise NotFoundError("payment method with token " + payment_method_token + " not found")

    def delete(self, payment_method_token):
        self.config.http().delete("/payment_methods/any/" + payment_method_token)
        return SuccessfulResult()

    def _post(self, url, params={}):
        response = self.config.http().post(url, params)
        if "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])
        else:
            payment_method = self._parse_payment_method(response)
            return SuccessfulResult({"payment_method": payment_method})

    def _put(self, url, params={}):
        response = self.config.http().put(url, params)
        if "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])
        else:
            payment_method = self._parse_payment_method(response)
            return SuccessfulResult({"payment_method": payment_method})

    def _parse_payment_method(self, response):
        if "paypal_account" in response:
            return PayPalAccount(self.gateway, response["paypal_account"])
        elif "credit_card" in response:
            return CreditCard(self.gateway, response["credit_card"])
        elif "sepa_bank_account" in response:
            return SEPABankAccount(self.gateway, response["sepa_bank_account"])
        else:
            name = list(response)[0]
            return UnknownPaymentMethod(self.gateway, response[name])
