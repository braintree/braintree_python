from braintree.resource import Resource
from braintree.paypal_payment_resource import PayPalPaymentResource
from braintree.payment_method_nonce import PaymentMethodNonce
from braintree.util.xml_util import XmlUtil
from braintree.error_result import ErrorResult
from braintree.successful_result import SuccessfulResult
from braintree.exceptions.unexpected_error import UnexpectedError

class PayPalPaymentResourceGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def update(self, params):
        Resource.verify_keys(params, PayPalPaymentResource.update_signature())

        response = self.config.http().put(
            self.config.base_merchant_path()  + "/paypal/payment_resource",
            params
        )

        if "payment_method_nonce" in response:
            return SuccessfulResult({"payment_method_nonce": PaymentMethodNonce(self.gateway, response["payment_method_nonce"])})
        elif "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])
        else:
            raise UnexpectedError("Couldn't parse response")

    
