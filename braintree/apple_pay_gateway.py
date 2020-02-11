try:
    from html import escape
except ImportError:
    from cgi import escape

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

        # NEXT_MAJOR_VERSION consider making this method align with the Ruby SDK
        # in the Ruby SDK, this is returned as an apple_pay_options object
        # https://github.com/braintree/braintree_ruby/blob/989b8f5acc42ab4fe634c818d692aec1d56daa36/lib/braintree/apple_pay_gateway.rb#L29
        if "response" in response:
            response = response["response"]

        return response["domains"]
