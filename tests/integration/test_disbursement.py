from tests.test_helper import *
from datetime import date

class TestDisbursement(unittest.TestCase):
    def test_disbursement_finds_transactions(self):
        disbursement = Disbursement(Configuration.gateway(), {
            "merchant_account": {
                "id": "sub_merchant_account",
                "status": "active",
                "master_merchant_account": {
                    "id": "master_merchant_account",
                    "status": "active"
                },
            },
            "id": "123456",
            "exception_message": "invalid_account_number",
            "amount": "100.00",
            "disbursement_date": date(2013, 4, 10),
            "follow_up_action": "update",
            "transaction_ids": ["sub_merchant_transaction"]
        })

        transactions = disbursement.transactions()
        self.assertEquals(1, transactions.maximum_size)
        self.assertEquals("sub_merchant_transaction", transactions.first.id)
