from tests.test_helper import *

class TestDisputes(unittest.TestCase):

    def test_find_returns_dispute_with_given_id(self):
        dispute = Dispute.find("open_dispute")

        self.assertEqual(dispute.amount_disputed, 31.0)
        self.assertEqual(dispute.amount_won, 0.0)
        self.assertEqual(dispute.id, "open_dispute")
        self.assertEqual(dispute.status, Dispute.Status.Open)
        self.assertEqual(dispute.transaction.id, "open_disputed_transaction")

    @raises_with_regexp(NotFoundError, "dispute with id 'invalid-id' not found")
    def test_find_raises_error_when_dispute_not_found(self):
        dispute = Dispute.find("invalid-id")
