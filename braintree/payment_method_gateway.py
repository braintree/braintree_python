import braintree
from braintree.apple_pay_card import ApplePayCard
from braintree.credit_card import CreditCard
from braintree.payment_method import PaymentMethod
from braintree.paypal_account import PayPalAccount
from braintree.europe_bank_account import EuropeBankAccount
from braintree.coinbase_account import CoinbaseAccount
from braintree.android_pay_card import AndroidPayCard
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
            if payment_method_token is None or payment_method_token.strip() == "":
                raise NotFoundError()

            response = self.config.http().get(self.config.base_merchant_path() + "/payment_methods/any/" + payment_method_token)
            return self._parse_payment_method(response)
        except NotFoundError:
            raise NotFoundError("payment method with token " + repr(payment_method_token) + " not found")

    def update(self, payment_method_token, params):
        Resource.verify_keys(params, PaymentMethod.update_signature())
        try:
            if payment_method_token is None or payment_method_token.strip() == "":
                raise NotFoundError()

            return self._put(
                "/payment_methods/any/" + payment_method_token,
                {"payment_method": params}
            )
        except NotFoundError:
            raise NotFoundError("payment method with token " + repr(payment_method_token) + " not found")

    def delete(self, payment_method_token):
        self.config.http().delete(self.config.base_merchant_path() + "/payment_methods/any/" + payment_method_token)
        return SuccessfulResult()

    def _post(self, url, params={}):
        response = self.config.http().post(self.config.base_merchant_path() + url, params)
        if "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])
        else:
            payment_method = self._parse_payment_method(response)
            return SuccessfulResult({"payment_method": payment_method})

    def _put(self, url, params={}):
        response = self.config.http().put(self.config.base_merchant_path() + url, params)
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
        elif "europe_bank_account" in response:
            return EuropeBankAccount(self.gateway, response["europe_bank_account"])
        elif "apple_pay_card" in response:
            return ApplePayCard(self.gateway, response["apple_pay_card"])
        elif "android_pay_card" in response:
            return AndroidPayCard(self.gateway, response["android_pay_card"])
        elif "coinbase_account" in response:
            return CoinbaseAccount(self.gateway, response["coinbase_account"])
        else:
            name = list(response)[0]
            return UnknownPaymentMethod(self.gateway, response[name])
