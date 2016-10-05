import braintree
from braintree.resource import Resource
from braintree.configuration import Configuration

class UsBankAccount(Resource):

    @staticmethod
    def find(token):
        return Configuration.gateway().us_bank_account.find(token)

    @staticmethod
    def sale(token, transactionRequest):
        transactionRequest["payment_method_token"] = token
        if not "options" in transactionRequest:
            transactionRequest["options"] = {}
        transactionRequest["options"]["submit_for_settlement"] = True
        return Configuration.gateway().transaction.sale(transactionRequest)

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
