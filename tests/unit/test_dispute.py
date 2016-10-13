from tests.test_helper import *
from datetime import date
from braintree.dispute import Dispute

class TestDispute(unittest.TestCase):
    def test_constructor(self):
        attributes = {
            "transaction": {
                "id": "transaction_id",
                "amount": "100.00",
            },
            "id": "123456",
            "currency_iso_code": "USD",
            "status": "open",
            "amount": "100.00",
            "received_date": date(2013, 4, 10),
            "reply_by_date": date(2013, 4, 10),
            "reason": "fraud",
            "transaction_ids": ["asdf", "qwer"],
            "date_opened": date(2013, 4, 1),
            "date_won": date(2013, 4, 2),
            "kind": "chargeback",
        }

        dispute = Dispute(attributes)

        self.assertEqual(dispute.id, "123456")
        self.assertEqual(dispute.amount, Decimal("100.00"))
        self.assertEqual(dispute.currency_iso_code, "USD")
        self.assertEqual(dispute.reason, Dispute.Reason.Fraud)
        self.assertEqual(dispute.status, Dispute.Status.Open)
        self.assertEqual(dispute.transaction_details.id, "transaction_id")
        self.assertEqual(dispute.transaction_details.amount, Decimal("100.00"))
        self.assertEqual(dispute.date_opened, date(2013, 4, 1))
        self.assertEqual(dispute.date_won, date(2013, 4, 2))
        self.assertEqual(dispute.kind, Dispute.Kind.Chargeback)
