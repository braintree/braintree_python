import braintree
from braintree.apple_pay_card import ApplePayCard
from braintree.credit_card import CreditCard
from braintree.payment_method import PaymentMethod
from braintree.paypal_account import PayPalAccount
from braintree.europe_bank_account import EuropeBankAccount
from braintree.coinbase_account import CoinbaseAccount
from braintree.android_pay_card import AndroidPayCard
from braintree.amex_express_checkout_card import AmexExpressCheckoutCard
from braintree.venmo_account import VenmoAccount
from braintree.us_bank_account import UsBankAccount
from braintree.visa_checkout_card import VisaCheckoutCard
from braintree.masterpass_card import MasterpassCard
from braintree.samsung_pay_card import SamsungPayCard
from braintree.unknown_payment_method import UnknownPaymentMethod
from braintree.error_result import ErrorResult
from braintree.exceptions.not_found_error import NotFoundError
from braintree.ids_search import IdsSearch
from braintree.payment_method_nonce import PaymentMethodNonce
from braintree.payment_method_parser import parse_payment_method
from braintree.resource import Resource
from braintree.resource_collection import ResourceCollection
from braintree.successful_result import SuccessfulResult

import sys
if sys.version_info[0] == 2:
    from urllib import urlencode
else:
    from urllib.parse import urlencode

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
            return parse_payment_method(self.gateway, response)
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

    def delete(self, payment_method_token, options={}):
        Resource.verify_keys(options, PaymentMethod.delete_signature())
        query_param = ""
        if options:
            if 'revoke_all_grants' in options:
                options['revoke_all_grants'] = str(options['revoke_all_grants']).lower()
            query_param = "?" + urlencode(options)

        self.config.http().delete(self.config.base_merchant_path() + "/payment_methods/any/" + payment_method_token + query_param)
        return SuccessfulResult()

    def grant(self, payment_method_token, options=None):
        if payment_method_token is None or not str(payment_method_token).strip():
            raise ValueError("payment method token cannot be empty or blank")

        try:
            if isinstance(options, bool):
                options = { "allow_vaulting": options }
            elif options is None:
                options = {}
            self.options = options

            params = {
                       "payment_method": {
                           "shared_payment_method_token": payment_method_token
                        }
                     }
            params["payment_method"].update(options),

            return self._post(
                "/payment_methods/grant",
                params,
                "payment_method_nonce"
            )
        except NotFoundError:
            raise NotFoundError("payment method with payment_method_token " + repr(payment_method_token) + " not found")

    def revoke(self, payment_method_token):
        if payment_method_token is None or not str(payment_method_token).strip():
            raise ValueError

        try:
            return self._post(
                "/payment_methods/revoke",
                {
                    "payment_method": {
                        "shared_payment_method_token": payment_method_token
                    }
                },
                "revoke"
            )
        except NotFoundError:
            raise NotFoundError("payment method with payment_method_token " + repr(payment_method_token) + " not found")

    def _post(self, url, params={}, result_key="payment_method"):
        response = self.config.http().post(self.config.base_merchant_path() + url, params)
        if "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])
        elif result_key is "revoke" and response.get("success", False):
            return SuccessfulResult()
        elif result_key is "payment_method_nonce":
            payment_method_nonce = self._parse_payment_method_nonce(response)
            return SuccessfulResult({result_key: payment_method_nonce})
        else:
            payment_method = parse_payment_method(self.gateway, response)
            return SuccessfulResult({result_key: payment_method})
        return response

    def _put(self, url, params={}):
        response = self.config.http().put(self.config.base_merchant_path() + url, params)
        if "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])
        else:
            payment_method = parse_payment_method(self.gateway, response)
            return SuccessfulResult({"payment_method": payment_method})

    def _parse_payment_method_nonce(self, response):
        if "payment_method_nonce" in response:
            return PaymentMethodNonce(self.gateway, response["payment_method_nonce"])
        raise ValueError("payment_method_nonce not present in response")
