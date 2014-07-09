from tests.test_helper import *
from braintree.test.nonces import Nonces

class TestTestHelper(unittest.TestCase):
    def setUp(self):
        self.transaction = Transaction.sale({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "cvv": "100"
            },
            "amount": "100.00",
            "options": {
                "submit_for_settlement": "true"
            }
        }).transaction

    def test_settle_transaction_settles_transaction(self):
        TestHelper.settle_transaction(self.transaction.id)
        self.assertEquals(Transaction.Status.Settled, Transaction.find(self.transaction.id).status)

    def test_settlement_confirm_transaction(self):
        TestHelper.settlement_confirm_transaction(self.transaction.id)
        self.assertEquals(Transaction.Status.SettlementConfirmed, Transaction.find(self.transaction.id).status)

    def test_settlement_decline_transaction(self):
        TestHelper.settlement_decline_transaction(self.transaction.id)
        self.assertEquals(Transaction.Status.SettlementDeclined, Transaction.find(self.transaction.id).status)

