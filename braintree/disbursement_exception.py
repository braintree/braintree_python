from braintree.resource import Resource
from braintree.transaction_search import TransactionSearch
from decimal import Decimal

class DisbursementException(Resource):
    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        self.amount = Decimal(self.amount)
        self._memoized_merchant_account = None

    def __repr__(self):
        detail_list = ["amount", "disbursement_date", "message", "follow_up_action", "id"]
        return super(DisbursementException, self).__repr__(detail_list)

    @property
    def merchant_account(self):
        if not self._memoized_merchant_account:
            self._memoized_merchant_account = self.gateway.merchant_account.find(self.merchant_account_id)
        return self._memoized_merchant_account

    @property
    def transactions(self):
        return self.gateway.transaction.search([
            TransactionSearch.merchant_account_id == self.merchant_account_id,
            TransactionSearch.disbursement_date == self.disbursement_date
        ])


