import braintree
from braintree.resource import Resource
from braintree.configuration import Configuration

class PaymentMethod(Resource):
    @staticmethod
    def create(params={}):
        return Configuration.gateway().payment_method.create(params)

    @staticmethod
    def find(payment_method_token):
        return Configuration.gateway().payment_method.find(payment_method_token)

    @staticmethod
    def delete(payment_method_token):
        return Configuration.gateway().payment_method.delete(payment_method_token)

    @staticmethod
    def create_signature():
        return PaymentMethod.signature("create")

    @staticmethod
    def signature(type):
        signature = [
            "customer_id",
            "payment_method_nonce",
            "token",
            {"options": ["make_default"]}
        ]
        return signature
