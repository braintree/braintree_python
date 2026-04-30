import warnings
from braintree.error_result import ErrorResult
from braintree.successful_result import SuccessfulResult
from braintree.merchant import Merchant
from braintree.oauth_credentials import OAuthCredentials


class MerchantGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    # NEXT_MAJOR_VERSION remove this method
    # The merchant create endpoint has been disabled and this method will be removed in a future major version
    def create(self, params):
        warnings.warn("gateway.merchant.create(...) is deprecated and will be removed in a future version.", DeprecationWarning)
        return self.__create_merchant(params)

    def __create_merchant(self, params=None):
        if params is None:
            params = {}
        response = self.config.http().post("/merchants/create_via_api", {
            "merchant": params
        })

        if "response" in response and "merchant" in response["response"]:
            return SuccessfulResult({
                "merchant": Merchant(self.gateway, response["response"]["merchant"]),
                "credentials": OAuthCredentials(self.gateway, response["response"]["credentials"])
            })
        else:
            return ErrorResult(self.gateway, response["api_error_response"])
