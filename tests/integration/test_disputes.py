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
        }).document_upload

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

        dispute_from_transaction = Transaction.find(dispute.transaction.id).disputes[0]

        self.assertEqual(dispute_from_transaction.status, Dispute.Status.Accepted)

    def test_accept_errors_when_dispute_not_open(self):
        result = Dispute.accept("wells_dispute")

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("dispute")[0].code, ErrorCodes.Dispute.CanOnlyAcceptOpenDispute)
        self.assertEqual(result.errors.for_object("dispute")[0].message, "Disputes can only be accepted when they are in an Open state")

    def test_accept_raises_error_when_dispute_not_found(self):
        with self.assertRaisesRegex(NotFoundError, "dispute with id 'invalid-id' not found"):
            dispute = Dispute.accept("invalid-id")

    def test_add_file_evidence_adds_evidence(self):
        dispute = self.create_sample_dispute()
        document = self.create_evidence_document()

        result = Dispute.add_file_evidence(dispute.id, document.id)

        self.assertTrue(result.is_success)

        updated_dispute = Dispute.find(dispute.id)

        self.assertEqual(updated_dispute.evidence[0].id, result.evidence.id)

    def test_add_file_evidence_adds_category_file_evidence(self):
        dispute = self.create_sample_dispute()
        document = self.create_evidence_document()

        result = Dispute.add_file_evidence(dispute.id, { "document_id": document.id, "category": "GENERAL" })

        self.assertTrue(result.is_success)
        self.assertEqual(result.evidence.category, "GENERAL")

    def test_add_file_evidence_raises_error_when_dispute_not_found(self):
        with self.assertRaisesRegex(NotFoundError, "dispute with id 'unknown_dispute_id' not found"):
            dispute = Dispute.add_file_evidence("unknown_dispute_id", "text evidence")

    def test_add_file_evidence_raises_error_when_dispute_not_open(self):
        dispute = self.create_sample_dispute()
        document = self.create_evidence_document()

        Dispute.accept(dispute.id)

        result = Dispute.add_file_evidence(dispute.id, document.id)

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("dispute")[0].code, ErrorCodes.Dispute.CanOnlyAddEvidenceToOpenDispute)
        self.assertEqual(result.errors.for_object("dispute")[0].message, "Evidence can only be attached to disputes that are in an Open state")

    def test_categorized_file_evidence_for_text_only_category(self):
        dispute = self.create_sample_dispute()
        document = self.create_evidence_document()

        result = Dispute.add_file_evidence(dispute.id, { "document_id": document.id, "category": "DEVICE_ID" })

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("dispute")[0].code, ErrorCodes.Dispute.EvidenceCategoryTextOnly)
        self.assertEqual(result.errors.for_object("dispute")[0].message, "Only text evidence can be provided for this category")

    def test_categorized_file_evidence_with_unsupported_category(self):
        dispute = self.create_sample_dispute()
        document = self.create_evidence_document()

        result = Dispute.add_file_evidence(dispute.id, { "document_id": document.id, "category": "DOESNOTEXIST" })

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("dispute")[0].code, ErrorCodes.Dispute.CanOnlyCreateEvidenceWithValidCategory)
        self.assertEqual(result.errors.for_object("dispute")[0].message, "The category you supplied on the evidence record is not valid")

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
        self.assertIsNone(evidence.category)
        self.assertIsNone(evidence.sequence_number)

    def test_add_text_evidence_adds_category_and_sequence_number_text_evidence(self):
        dispute = self.create_sample_dispute()

        result = Dispute.add_text_evidence(dispute.id, { "content": "PROOF_OF_FULFILLMENT", "category": "DEVICE_ID", "sequence_number": "0" })

        self.assertTrue(result.is_success)
        evidence = result.evidence
        self.assertEqual(evidence.comment, "PROOF_OF_FULFILLMENT")
        self.assertEqual(evidence.category, "DEVICE_ID")
        self.assertEqual(evidence.sequence_number, 0)

    def test_add_text_evidence_raises_error_when_dispute_not_found(self):
        with self.assertRaisesRegex(NotFoundError, "Dispute with ID 'unknown_dispute_id' not found"):
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

    def test_categorized_text_evidence_with_unsupported_category(self):
        dispute = self.create_sample_dispute()
        result = Dispute.add_text_evidence(dispute.id, { "content": "evidence", "category": "DOESNOTEXIST" })

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("dispute")[0].code, ErrorCodes.Dispute.CanOnlyCreateEvidenceWithValidCategory)
        self.assertEqual(result.errors.for_object("dispute")[0].message, "The category you supplied on the evidence record is not valid")

    def test_categorized_text_evidence_with_file_category(self):
        dispute = self.create_sample_dispute()
        result = Dispute.add_text_evidence(dispute.id, { "content": "evidence", "category": "MERCHANT_WEBSITE_OR_APP_ACCESS" })

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("dispute")[0].code, ErrorCodes.Dispute.EvidenceCategoryDocumentOnly)
        self.assertEqual(result.errors.for_object("dispute")[0].message, "Only document evidence can be provided for this category")

    def test_categorized_text_evidence_with_invalid_date_time_format(self):
        dispute = self.create_sample_dispute()
        result = Dispute.add_text_evidence(dispute.id, { "content": "not a date", "category": "DOWNLOAD_DATE_TIME" })

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("dispute")[0].code, ErrorCodes.Dispute.EvidenceContentDateInvalid)

    def test_categorized_text_evidence_with_valid_date_time_format(self):
        dispute = self.create_sample_dispute()
        result = Dispute.add_text_evidence(dispute.id, { "content": "2018-10-20T18:00:00-0500", "category": "DOWNLOAD_DATE_TIME" })

        self.assertTrue(result.is_success)

    def test_add_text_evidence_adds_category_and_shipping_tracking_carrier_name(self):
        dispute = self.create_sample_dispute()

        result = Dispute.add_text_evidence(dispute.id, { "content": "UPS", "category": "CARRIER_NAME", "sequence_number": "0" })

        self.assertTrue(result.is_success)
        evidence = result.evidence
        self.assertEqual(evidence.comment, "UPS")
        self.assertEqual(evidence.category, "CARRIER_NAME")
        self.assertEqual(evidence.sequence_number, 0)

    def test_add_text_evidence_adds_category_and_shipping_tracking_tracking_number(self):
        dispute = self.create_sample_dispute()

        result = Dispute.add_text_evidence(dispute.id, { "content": "3", "category": "TRACKING_NUMBER", "sequence_number": "0" })

        self.assertTrue(result.is_success)
        evidence = result.evidence
        self.assertEqual(evidence.comment, "3")
        self.assertEqual(evidence.category, "TRACKING_NUMBER")
        self.assertEqual(evidence.sequence_number, 0)

    def test_add_text_evidence_adds_category_and_shipping_tracking_tracking_url(self):
        dispute = self.create_sample_dispute()

        result = Dispute.add_text_evidence(dispute.id, { "content": "https://example.com/tracking-number/abc12345", "category": "TRACKING_URL", "sequence_number": "1" })

        self.assertTrue(result.is_success)
        evidence = result.evidence
        self.assertEqual(evidence.comment, "https://example.com/tracking-number/abc12345")
        self.assertEqual(evidence.category, "TRACKING_URL")
        self.assertEqual(evidence.sequence_number, 1)

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

    def test_finalize_when_digital_goods_missing(self):
        dispute = self.create_sample_dispute()
        result = Dispute.add_text_evidence(dispute.id, { "content": "device_id", "category": "DEVICE_ID" })

        self.assertTrue(result.is_success)

        result = dispute.finalize(dispute.id)

        self.assertFalse(result.is_success)

        error_codes = [error.code for error in result.errors.for_object("dispute")]
        self.assertIn(ErrorCodes.Dispute.DigitalGoodsMissingDownloadDate, error_codes)
        self.assertIn(ErrorCodes.Dispute.DigitalGoodsMissingEvidence, error_codes)

    def test_finalize_when_missing_non_disputed_payments_date(self):
        dispute = self.create_sample_dispute()
        result = Dispute.add_text_evidence(dispute.id, { "content": "123", "category": "PRIOR_NON_DISPUTED_TRANSACTION_ARN" })

        self.assertTrue(result.is_success)

        result = dispute.finalize(dispute.id)

        self.assertFalse(result.is_success)

        error_codes = [error.code for error in result.errors.for_object("dispute")]
        self.assertIn(ErrorCodes.Dispute.NonDisputedPriorTransactionEvidenceMissingDate, error_codes)

    def test_finalize_raises_error_when_dispute_not_found(self):
        with self.assertRaisesRegex(NotFoundError, "dispute with id 'invalid-id' not found"):
            dispute = Dispute.finalize("invalid-id")

    def test_find_returns_dispute_with_given_id(self):
        dispute = Dispute.find("open_dispute")

        self.assertEqual(dispute.amount_disputed, 31.0)
        self.assertEqual(dispute.amount_won, 0.0)
        self.assertEqual(dispute.id, "open_dispute")
        self.assertEqual(dispute.status, Dispute.Status.Open)
        self.assertEqual(dispute.transaction.id, "open_disputed_transaction")
        self.assertEqual(None, dispute.transaction.installment_count)
        self.assertNotEqual(None, dispute.graphql_id)
        
    def test_dispute_contains_remaining_file_evidence_storage(self):
        dispute = self.create_sample_dispute()
        
        self.assertIsNotNone(dispute.remaining_file_evidence_storage)
        self.assertTrue(isinstance(dispute.remaining_file_evidence_storage, int))
        
    def test_remaining_file_evidence_storage_changes_after_file_evidence_addition(self):
        dispute = self.create_sample_dispute()
        
        initial_storage = dispute.remaining_file_evidence_storage
        self.assertIsNotNone(initial_storage)
        initial_storage_value = int(initial_storage)
        
        document = self.create_evidence_document()
        
        result = Dispute.add_file_evidence(dispute.id, document.id)
        self.assertTrue(result.is_success)
        
        updated_dispute = Dispute.find(dispute.id)
        
        self.assertIsNotNone(updated_dispute.remaining_file_evidence_storage)
        updated_storage_value = int(updated_dispute.remaining_file_evidence_storage)
        
        self.assertLess(updated_storage_value, initial_storage_value)

    def test_find_raises_error_when_dispute_not_found(self):
        with self.assertRaisesRegex(NotFoundError, "dispute with id 'invalid-id' not found"):
            dispute = Dispute.find("invalid-id")

    def test_delete_customer_with_path_traversal(self):
        try:
            customer = Customer.create({"first_name":"Waldo"}).customer
            dispute = self.create_sample_dispute()
            Dispute.remove_evidence(dispute.id, "../../../customers/{}".format(customer.id))
        except NotFoundError:
            pass

        found_customer = Customer.find(customer.id)
        self.assertNotEqual(None, found_customer)
        self.assertEqual("Waldo", found_customer.first_name)


    def test_remove_evidence_removes_evidence_from_the_dispute(self):
        dispute = self.create_sample_dispute()
        evidence = Dispute.add_text_evidence(dispute.id, "text evidence").evidence
        result = Dispute.remove_evidence(dispute.id, evidence.id)

        self.assertTrue(result.is_success)

    def test_remove_evidence_raises_error_when_dispute_or_evidence_not_found(self):
        with self.assertRaisesRegex(NotFoundError, "evidence with id 'unknown_evidence_id' for dispute with id 'unknown_dispute_id' not found"):
            Dispute.remove_evidence("unknown_dispute_id", "unknown_evidence_id")

    def test_remove_evidence_errors_when_dispute_not_open(self):
        dispute = self.create_sample_dispute()
        evidence = Dispute.add_text_evidence(dispute.id, "text evidence").evidence

        Dispute.accept(dispute.id)

        result = Dispute.remove_evidence(dispute.id, evidence.id)

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("dispute")[0].code, ErrorCodes.Dispute.CanOnlyRemoveEvidenceFromOpenDispute)
        self.assertEqual(result.errors.for_object("dispute")[0].message, "Evidence can only be removed from disputes that are in an Open state")
