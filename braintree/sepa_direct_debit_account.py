import braintree
from braintree.resource import Resource
from braintree.configuration import Configuration


class SepaDirectDebitAccount(Resource):
    @staticmethod
    def find(sepa_direct_debit_account_token):
        return Configuration.gateway().sepa_direct_debit_account.find(sepa_direct_debit_account_token)

    @staticmethod
    def delete(sepa_direct_debit_account_token):
        return Configuration.gateway().sepa_direct_debit_account.delete(sepa_direct_debit_account_token)

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        if "subscriptions" in attributes:
            self.subscriptions = [braintree.subscription.Subscription(gateway, subscription) for subscription in self.subscriptions]
