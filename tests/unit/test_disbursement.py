from tests.test_helper import *
from datetime import date

class TestDisbursement(unittest.TestCase):
    attributes = {
        "merchant_account": {
            "id": "merchant_account",
            "status": "active",
        },
        "id": "123456",
        "exception_message": "invalid_account_number",
        "amount": "100.00",
        "disbursement_date": date(2013, 4, 10),
        "follow_up_action": "update",
        "transaction_ids": ["asdf", "qwer"],
        "disbursement_type": "credit"
    }

    def test_constructor(self):
        disbursement = Disbursement(None, TestDisbursement.attributes)

        self.assertEqual("123456", disbursement.id)
        self.assertEqual(Decimal("100.00"), disbursement.amount)
        self.assertEqual(["asdf", "qwer"], disbursement.transaction_ids)
        self.assertEqual("active", disbursement.merchant_account.status)
        self.assertEqual("merchant_account", disbursement.merchant_account.id)

    def test_credit(self):
        disbursement = Disbursement(None, TestDisbursement.attributes)

        self.assertTrue(disbursement.is_credit())

    def test_debit(self):
        thing = TestDisbursement.attributes
        thing["disbursement_type"] = "debit"

        disbursement = Disbursement(None, TestDisbursement.attributes)

        self.assertTrue(disbursement.is_debit())
