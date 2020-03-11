try:
    from html import escape
except ImportError:
    from cgi import escape

from braintree.apple_pay_options import ApplePayOptions
from braintree.error_result import ErrorResult
from braintree.successful_result import SuccessfulResult
from braintree.exceptions.unexpected_error import UnexpectedError

class ApplePayGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def register_domain(self, domain):
        response = self.config.http().post(self.config.base_merchant_path() + "/processing/apple_pay/validate_domains", {'url': domain})

        if "response" in response and response["response"]["success"]:
            return SuccessfulResult()
        elif response["api_error_response"]:
            return ErrorResult(self.gateway, response["api_error_response"])

    def unregister_domain(self, domain):
        self.config.http().delete(self.config.base_merchant_path() + "/processing/apple_pay/unregister_domain?url=" + escape(domain))
        return SuccessfulResult()

    def registered_domains(self):
        response = self.config.http().get(self.config.base_merchant_path() + "/processing/apple_pay/registered_domains")

        if "response" in response:
            response = ApplePayOptions(response.pop("response"))

        return response.domains
