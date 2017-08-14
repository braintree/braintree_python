import re
import time
import datetime
from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers

class TestDisputes(unittest.TestCase):
    def create_evidence_document(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "fixtures/bt_logo.png")
        png_file = open(file_path, "rb")

        return DocumentUpload.create({
            "kind": braintree.DocumentUpload.Kind.EvidenceDocument,
            "file": png_file
        }).document

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

    def test_add_file_evidence_adds_evidence(self):
        dispute = self.create_sample_dispute()
        document = self.create_evidence_document()

        result = Dispute.add_file_evidence(dispute.id, document.id)

        self.assertTrue(result.is_success)

        updated_dispute = Dispute.find(dispute.id)

        self.assertEqual(updated_dispute.evidence[0].id, result.evidence.id)

    @raises_with_regexp(NotFoundError, "dispute with id 'unknown_dispute_id' not found")
    def test_add_file_evidence_raises_error_when_dispute_not_found(self):
        dispute = Dispute.add_file_evidence("unknown_dispute_id", "text evidence")

    def test_add_file_evidence_raises_error_when_dispute_not_open(self):
        dispute = self.create_sample_dispute()
        document = self.create_evidence_document()

        Dispute.accept(dispute.id)

        result = Dispute.add_file_evidence(dispute.id, document.id)

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("dispute")[0].code, ErrorCodes.Dispute.CanOnlyAddEvidenceToOpenDispute)
        self.assertEqual(result.errors.for_object("dispute")[0].message, "Evidence can only be attached to disputes that are in an Open state")

    def test_add_file_evidence_returns_error_when_incorrect_document_kind(self):
        dispute = self.create_sample_dispute()
        file_path = os.path.join(os.path.dirname(__file__), "..", "fixtures/bt_logo.png")
        png_file = open(file_path, "rb")

        document = DocumentUpload.create({
            "kind": braintree.DocumentUpload.Kind.IdentityDocument,
            "file": png_file
        }).document

        result = Dispute.add_file_evidence(dispute.id, document.id)

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("dispute")[0].code, ErrorCodes.Dispute.CanOnlyAddEvidenceDocumentToDispute)

    def test_add_text_evidence_adds_text_evidence(self):
        dispute = self.create_sample_dispute()

        result = Dispute.add_text_evidence(dispute.id, "text evidence")
        evidence = result.evidence

        self.assertTrue(result.is_success)
        self.assertEqual(evidence.comment, "text evidence")
        self.assertIsNotNone(evidence.created_at)
        self.assertTrue(re.match("^\w{16,}$", evidence.id))
        self.assertIsNone(evidence.sent_to_processor_at)
        self.assertIsNone(evidence.url)

    @raises_with_regexp(NotFoundError, "dispute with id 'unknown_dispute_id' not found")
    def test_add_text_evidence_raises_error_when_dispute_not_found(self):
        dispute = Dispute.add_text_evidence("unknown_dispute_id", "text evidence")

    def test_add_text_evidence_raises_error_when_dispute_not_open(self):
        dispute = self.create_sample_dispute()

        Dispute.accept(dispute.id)
        result = Dispute.add_text_evidence(dispute.id, "text evidence")

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("dispute")[0].code, ErrorCodes.Dispute.CanOnlyAddEvidenceToOpenDispute)
        self.assertEqual(result.errors.for_object("dispute")[0].message, "Evidence can only be attached to disputes that are in an Open state")

    def test_add_text_evidence_shows_new_record_in_find(self):
        dispute = self.create_sample_dispute()

        evidence = Dispute.add_text_evidence(dispute.id, "text evidence").evidence

        refreshed_dispute = Dispute.find(dispute.id)

        self.assertEqual(refreshed_dispute.evidence[0].id, evidence.id)
        self.assertEqual(refreshed_dispute.evidence[0].comment, "text evidence")

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

    def test_remove_evidence_removes_evidence_from_the_dispute(self):
        dispute = self.create_sample_dispute()
        evidence = Dispute.add_text_evidence(dispute.id, "text evidence").evidence
        result = Dispute.remove_evidence(dispute.id, evidence.id)

        self.assertTrue(result.is_success)

    @raises_with_regexp(NotFoundError, "evidence with id 'unknown_evidence_id' for dispute with id 'unknown_dispute_id' not found")
    def test_remove_evidence_raises_error_when_dispute_or_evidence_not_found(self):
        Dispute.remove_evidence("unknown_dispute_id", "unknown_evidence_id")

    def test_remove_evidence_errors_when_dispute_not_open(self):
        dispute = self.create_sample_dispute()
        evidence = Dispute.add_text_evidence(dispute.id, "text evidence").evidence

        Dispute.accept(dispute.id)

        result = Dispute.remove_evidence(dispute.id, evidence.id)

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("dispute")[0].code, ErrorCodes.Dispute.CanOnlyRemoveEvidenceFromOpenDispute)
        self.assertEqual(result.errors.for_object("dispute")[0].message, "Evidence can only be removed from disputes that are in an Open state")
