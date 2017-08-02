from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers

class TestDisputes(unittest.TestCase):
    def create_sample_dispute(self):
        return Transaction.sale({
            "amount": "100.00",
            "credit_card": {
                "number": CreditCardNumbers.Disputes.Chargeback,
                "expiration_date": "12/2019"
            }
        }).transaction.disputes[0]

    def test_accept_changes_dispute_status_to_accepted(self):
        dispute = self.create_sample_dispute()

        result = Dispute.accept(dispute.id)

        self.assertTrue(result.is_success)

        updated_dispute = Dispute.find(dispute.id)

        self.assertEqual(updated_dispute.status, Dispute.Status.Accepted)

    def test_accept_errors_when_dispute_not_open(self):
        result = Dispute.accept("wells_dispute")

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("dispute")[0].code, ErrorCodes.Dispute.CanOnlyAcceptOpenDispute)
        self.assertEqual(result.errors.for_object("dispute")[0].message, "Disputes can only be accepted when they are in an Open state")

    @raises_with_regexp(NotFoundError, "dispute with id 'invalid-id' not found")
    def test_accept_raises_error_when_dispute_not_found(self):
        dispute = Dispute.accept("invalid-id")

    def test_finalize_changes_dispute_status_to_disputed(self):
        dispute = self.create_sample_dispute()

        result = Dispute.finalize(dispute.id)

        self.assertTrue(result.is_success)

        updated_dispute = Dispute.find(dispute.id)

        self.assertEqual(updated_dispute.status, Dispute.Status.Disputed)

    def test_finalize_errors_when_dispute_not_open(self):
        result = Dispute.finalize("wells_dispute")

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("dispute")[0].code, ErrorCodes.Dispute.CanOnlyFinalizeOpenDispute)
        self.assertEqual(result.errors.for_object("dispute")[0].message, "Disputes can only be finalized when they are in an Open state")

    @raises_with_regexp(NotFoundError, "dispute with id 'invalid-id' not found")
    def test_finalize_raises_error_when_dispute_not_found(self):
        dispute = Dispute.finalize("invalid-id")

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
