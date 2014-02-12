from braintree.resource import Resource
from braintree.transaction_search import TransactionSearch
from decimal import Decimal

class Transfer(Resource):
    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        self.amount = Decimal(self.amount)

    def __repr__(self):
        detail_list = ["amount", "disbursement_date", "message", "follow_up_action", "id"]
        return super(Transfer, self).__repr__(detail_list)

    @property
    def merchant_account(self):
        return self.gateway.merchant_account.find(self.merchant_account_id)

    @property
    def transactions(self):
        return self.gateway.transaction.search([
            TransactionSearch.merchant_account_id == self.merchant_account_id,
            TransactionSearch.disbursement_date == self.disbursement_date
        ])


