import braintree
from braintree.resource import Resource
from braintree.configuration import Configuration

class UsBankAccount(Resource):

    @staticmethod
    def signature():
        signature = [
            "routing_number",
            "last_4",
            "account_type",
            "account_description",
            "account_holder_name",
            "token",
            "image_url"
        ]
        return signature
