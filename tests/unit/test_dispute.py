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
            "transaction_ids": ["asdf", "qwer"]
        }

        dispute = Dispute(attributes)

        self.assertEquals(dispute.id, "123456")
        self.assertEquals(dispute.amount, Decimal("100.00"))
        self.assertEquals(dispute.currency_iso_code, "USD")
        self.assertEquals(dispute.reason, Dispute.Reason.Fraud)
        self.assertEquals(dispute.status, Dispute.Status.Open)
        self.assertEquals(dispute.transaction_details.id, "transaction_id")
        self.assertEquals(dispute.transaction_details.amount, Decimal("100.00"))
