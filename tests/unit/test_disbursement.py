from tests.test_helper import *
from datetime import date

class TestDisbursement(unittest.TestCase):
    def test_constructor(self):
        attributes = {
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
            "transaction_ids": ["asdf", "qwer"]
        }

        disbursement = Disbursement(None, attributes)

        self.assertEqual("123456", disbursement.id)
        self.assertEqual(Decimal("100.00"), disbursement.amount)
        self.assertEqual(["asdf", "qwer"], disbursement.transaction_ids)
        self.assertEqual("master_merchant_account", disbursement.merchant_account.master_merchant_account.id)
