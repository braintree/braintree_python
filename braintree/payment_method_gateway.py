import braintree
from braintree.apple_pay_card import ApplePayCard
from braintree.credit_card import CreditCard
from braintree.payment_method import PaymentMethod
from braintree.paypal_account import PayPalAccount
from braintree.europe_bank_account import EuropeBankAccount
from braintree.android_pay_card import AndroidPayCard
# NEXT_MAJOR_VERSION remove amex express checkout
from braintree.amex_express_checkout_card import AmexExpressCheckoutCard
from braintree.sepa_direct_debit_account import SepaDirectDebitAccount
from braintree.venmo_account import VenmoAccount
from braintree.us_bank_account import UsBankAccount
from braintree.visa_checkout_card import VisaCheckoutCard
# NEXT_MAJOR_VERSION remove masterpass
from braintree.masterpass_card import MasterpassCard
# NEXT_MAJOR_VERSION remove SamsungPayCard
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
from urllib.parse import urlencode


class PaymentMethodGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def create(self, params=None):
        if params is None:
            params = {}
        Resource.verify_keys(params, PaymentMethod.create_signature())
        self.__check_for_deprecated_attributes(params);
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
        self.__check_for_deprecated_attributes(params);
        try:
            if payment_method_token is None or payment_method_token.strip() == "":
                raise NotFoundError()

            return self._put(
                "/payment_methods/any/" + payment_method_token,
                {"payment_method": params}
            )
        except NotFoundError:
            raise NotFoundError("payment method with token " + repr(payment_method_token) + " not found")

    def delete(self, payment_method_token, options=None):
        if options is None:
            options = {}
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

    def _post(self, url, params=None, result_key="payment_method"):
        if params is None:
            params = {}
        response = self.config.http().post(self.config.base_merchant_path() + url, params)
        if "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])
        elif result_key == "revoke" and response.get("success", False):
            return SuccessfulResult()
        elif result_key == "payment_method_nonce":
            payment_method_nonce = self._parse_payment_method_nonce(response)
            return SuccessfulResult({result_key: payment_method_nonce})
        else:
            payment_method = parse_payment_method(self.gateway, response)
            return SuccessfulResult({result_key: payment_method})
        return response

    def _put(self, url, params=None):
        if params is None:
            params = {}
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

    # NEXT_MAJOR_VERSION remove these checks when the attributes are removed
    def __check_for_deprecated_attributes(self, params):
        if "device_session_id" in params.keys():
            warnings.warn("device_session_id is deprecated, use device_data parameter instead", DeprecationWarning)
        if "fraud_merchant_id" in params.keys():
            warnings.warn("fraud_merchant_id is deprecated, use device_data parameter instead", DeprecationWarning)
        if "venmo_sdk_payment_method_code" in params.keys() or "venmo_sdk_session" in params.keys():
            warnings.warn("The Venmo SDK integration is Unsupported. Please update your integration to use Pay with Venmo instead.", DeprecationWarning)
        if "samsung_pay_card" in params.keys():
            warnings.warn("SamsungPay is deprecated", DeprecationWarning)

