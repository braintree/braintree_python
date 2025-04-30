from tests.test_helper import *
from datetime import date

class TestDisbursement(unittest.TestCase):
    def test_disbursement_finds_transactions(self):
        disbursement = Disbursement(Configuration.gateway(), {
            "merchant_account": {
                "id": "ma_card_processor_brazil",
                "status": "active",

            },
            "id": "123456",
            "exception_message": "invalid_account_number",
            "amount": "100.00",
            "disbursement_date": date(2013, 4, 10),
            "follow_up_action": "update",
            "transaction_ids": ["transaction_with_installments_and_adjustments"]
        })

        transactions = disbursement.transactions()
        self.assertEqual(1, transactions.maximum_size)
        self.assertEqual("transaction_with_installments_and_adjustments", transactions.first.id)
