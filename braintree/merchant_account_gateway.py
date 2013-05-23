import re
import braintree
from braintree.merchant_account import MerchantAccount
from braintree.error_result import ErrorResult
from braintree.resource import Resource
from braintree.successful_result import SuccessfulResult

class MerchantAccountGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def create(self, params={}):
        Resource.verify_keys(params, MerchantAccount.create_signature())

        response = self.config.http().post("/merchant_accounts/create_via_api", {"merchant_account": params})
        if "merchant_account" in response:
            return SuccessfulResult({"merchant_account": MerchantAccount(self.gateway, response["merchant_account"])})
        elif "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])

