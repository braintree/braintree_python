import braintree
from braintree.resource import Resource
from braintree.configuration import Configuration

class PayPalAccount(Resource):
    @staticmethod
    def find(paypal_account_token):
        return Configuration.gateway().paypal_account.find(paypal_account_token)

    @staticmethod
    def delete(paypal_account_token):
        return Configuration.gateway().paypal_account.delete(paypal_account_token)

    @staticmethod
    def update(paypal_account_token, params={}):
        return Configuration.gateway().paypal_account.update(paypal_account_token, params)

    @staticmethod
    def signature():
        signature = [
            "token",
            {"options": ["make_default"]}
        ]
        return signature
