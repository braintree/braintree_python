import braintree
from braintree.resource import Resource
from braintree.configuration import Configuration

class PaymentMethodNonce(Resource):
    @staticmethod
    def create(payment_method_token):
        return Configuration.gateway().payment_method_nonce.create(payment_method_token)
