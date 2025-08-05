from tests.test_helper import *
from datetime import date
from braintree.dispute import Dispute

class TestDispute(unittest.TestCase):
    legacy_attributes = {
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

    attributes = {
        "amount": "100.00",
        "amount_disputed": "100.00",
        "amount_won": "0.00",
        "case_number": "CB123456",
        "chargeback_protection_level": "effortless",
        "created_at": datetime(2013, 4, 10, 10, 50, 39),
        "currency_iso_code": "USD",
        "date_opened": date(2013, 4, 1),
        "date_won": date(2013, 4, 2),
        "processor_comments": "Forwarded comments",
        "id": "123456",
        "kind": "chargeback",
        "merchant_account_id": "abc123",
        "original_dispute_id": "original_dispute_id",
        "pre_dispute_program": "none",
        "reason": "fraud",
        "reason_code": "83",
        "reason_description": "Reason code 83 description",
        "received_date": date(2013, 4, 10),
        "reference_number": "123456",
        "remaining_file_evidence_storage": "3189762",
        "reply_by_date": date(2013, 4, 17),
        "status": "open",
        "updated_at": datetime(2013, 4, 10, 10, 50, 39),
        "evidence": [{
            "comment": None,
            "created_at": datetime(2013, 4, 11, 10, 50, 39),
            "id": "evidence1",
            "sent_to_processor_at": None,
            "url": "url_of_file_evidence",
        },{
            "comment": "text evidence",
            "created_at": datetime(2013, 4, 11, 10, 50, 39),
            "id": "evidence2",
            "sent_to_processor_at": "2009-04-11",
            "url": None,
        }],
        "status_history": [{
            "disbursement_date": "2013-04-11",
            "effective_date": "2013-04-10",
            "status": "open",
            "timestamp": datetime(2013, 4, 10, 10, 50, 39),
        }],
        "transaction": {
            "id": "transaction_id",
            "amount": "100.00",
            "created_at": datetime(2013, 3, 19, 10, 50, 39),
            "installment_count": None,
            "order_id": None,
            "purchase_order_number": "po",
            "payment_instrument_subtype": "Visa",
        },
        "paypal_messages": [{
            "message": "message",
            "sender": "seller",
            "sent_at": datetime(2013, 4, 10, 10, 50, 39),
        }],
        # NEXT_MAJOR_VERSION remove deprecated evidence_submittable
        # DEPRECATED The evidence_submittable attribute is deprecated
        "evidence_submittable": True,
    }

    def test_legacy_constructor(self):
        dispute = Dispute(dict(self.legacy_attributes))

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

    def test_legacy_params_with_new_attributes(self):
        dispute = Dispute(dict(self.attributes))

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

    def test_constructor_populates_new_fields(self):
        attributes = dict(self.attributes)
        del attributes["amount"]

        dispute = Dispute(attributes)

        self.assertEqual(dispute.amount_disputed, 100.0)
        self.assertEqual(dispute.amount_won, 0.00)
        self.assertEqual(dispute.case_number, "CB123456")
        # NEXT_MAJOR_VERSION Remove this assertion when chargeback_protection_level is removed from the SDK
        self.assertEqual(dispute.chargeback_protection_level, "effortless")
        self.assertEqual(dispute.protection_level, braintree.Dispute.ProtectionLevel.EffortlessCBP)
        self.assertEqual(dispute.created_at, datetime(2013, 4, 10, 10, 50, 39))
        self.assertEqual(dispute.forwarded_comments, "Forwarded comments")
        self.assertEqual(dispute.processor_comments, "Forwarded comments")
        self.assertEqual(dispute.merchant_account_id, "abc123")
        self.assertEqual(dispute.original_dispute_id, "original_dispute_id")
        self.assertEqual(dispute.pre_dispute_program, Dispute.PreDisputeProgram.NONE)
        self.assertEqual(dispute.reason_code, "83")
        self.assertEqual(dispute.reason_description, "Reason code 83 description")
        self.assertEqual(dispute.reference_number, "123456")
        self.assertEqual(dispute.remaining_file_evidence_storage, "3189762")
        self.assertEqual(dispute.updated_at, datetime(2013, 4, 10, 10, 50, 39))
        self.assertIsNone(dispute.evidence[0].comment)
        self.assertEqual(dispute.evidence[0].created_at, datetime(2013, 4, 11, 10, 50, 39))
        self.assertEqual(dispute.evidence[0].id, "evidence1")
        self.assertIsNone(dispute.evidence[0].sent_to_processor_at)
        self.assertEqual(dispute.evidence[0].url, "url_of_file_evidence")
        self.assertEqual(dispute.evidence[1].comment, "text evidence")
        self.assertEqual(dispute.evidence[1].created_at, datetime(2013, 4, 11, 10, 50, 39))
        self.assertEqual(dispute.evidence[1].id, "evidence2")
        self.assertEqual(dispute.evidence[1].sent_to_processor_at, "2009-04-11")
        self.assertIsNone(dispute.evidence[1].url)
        self.assertEqual(dispute.paypal_messages[0].message, "message")
        self.assertEqual(dispute.paypal_messages[0].sender, "seller")
        self.assertEqual(dispute.paypal_messages[0].sent_at, datetime(2013, 4, 10, 10, 50, 39))
        self.assertEqual(dispute.status_history[0].disbursement_date, "2013-04-11")
        self.assertEqual(dispute.status_history[0].effective_date, "2013-04-10")
        self.assertEqual(dispute.status_history[0].status, "open")
        self.assertEqual(dispute.status_history[0].timestamp, datetime(2013, 4, 10, 10, 50, 39))
        # NEXT_MAJOR_VERSION remove deprecated evidence_submittable
        # DEPRECATED The evidence_submittable attribute is deprecated
        self.assertEqual(dispute.evidence_submittable, True)

    def test_constructor_populates_standard_cbp_level(self):
        attributes = dict(self.attributes)
        del attributes["amount"]
        attributes["chargeback_protection_level"] = "standard"

        dispute = Dispute(attributes)

        # NEXT_MAJOR_VERSION Remove this assertion when chargeback_protection_level is removed from the SDK
        self.assertEqual(dispute.chargeback_protection_level, braintree.Dispute.ChargebackProtectionLevel.Standard)
        self.assertEqual(dispute.protection_level, braintree.Dispute.ProtectionLevel.StandardCBP)

    def test_constructor_populates_none_cbp_level(self):
        attributes = dict(self.attributes)
        del attributes["amount"]
        attributes["chargeback_protection_level"] = None

        dispute = Dispute(attributes)

        # NEXT_MAJOR_VERSION Remove this assertion when chargeback_protection_level is removed from the SDK
        self.assertEqual(dispute.chargeback_protection_level, None)
        self.assertEqual(dispute.protection_level, braintree.Dispute.ProtectionLevel.NoProtection)

    def test_constructor_populates_empty_cbp_level(self):
        attributes = dict(self.attributes)
        del attributes["amount"]
        attributes["chargeback_protection_level"] = ""

        dispute = Dispute(attributes)

        # NEXT_MAJOR_VERSION Remove this assertion when chargeback_protection_level is removed from the SDK
        self.assertEqual(dispute.chargeback_protection_level, "")
        self.assertEqual(dispute.protection_level, braintree.Dispute.ProtectionLevel.NoProtection)

    def test_constructor_populates_not_protected_cbp_level(self):
        attributes = dict(self.attributes)
        del attributes["amount"]
        attributes["chargeback_protection_level"] = "not_protected"

        dispute = Dispute(attributes)

        # NEXT_MAJOR_VERSION Remove this assertion when chargeback_protection_level is removed from the SDK
        self.assertEqual(dispute.chargeback_protection_level, braintree.Dispute.ChargebackProtectionLevel.NotProtected)
        self.assertEqual(dispute.protection_level, braintree.Dispute.ProtectionLevel.NoProtection)

    def test_constructor_handles_none_fields(self):
        attributes = dict(self.attributes)
        attributes.update({
            "amount": None,
            "date_opened": None,
            "date_won": None,
            "evidence": None,
            "paypal_messages": None,
            "reply_by_date": None,
            "status_history": None
        })

        dispute = Dispute(attributes)

        self.assertIsNone(dispute.amount)
        self.assertIsNone(dispute.date_opened)
        self.assertIsNone(dispute.date_won)
        self.assertIsNone(dispute.evidence)
        self.assertIsNone(dispute.paypal_messages)
        self.assertIsNone(dispute.reply_by_date)
        self.assertIsNone(dispute.status_history)

    def test_constructor_populates_transaction(self):
        dispute = Dispute(dict(self.attributes))

        self.assertEqual(dispute.transaction.id, "transaction_id")
        self.assertEqual(dispute.transaction.amount, Decimal("100.00"))
        self.assertEqual(dispute.transaction.created_at, datetime(2013, 3, 19, 10, 50, 39))
        self.assertIsNone(dispute.transaction.installment_count)
        self.assertIsNone(dispute.transaction.order_id)
        self.assertEqual(dispute.transaction.purchase_order_number, "po")
        self.assertEqual(dispute.transaction.payment_instrument_subtype, "Visa")

    def test_accept_none_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "dispute with id None not found"):
            Dispute.accept(None)

    def test_accept_empty_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "dispute with id ' ' not found"):
            Dispute.accept(" ")

    def test_add_text_evidence_empty_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "dispute_id cannot be blank"):
            Dispute.add_text_evidence(" ", "evidence")

    def test_add_text_evidence_none_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "dispute_id cannot be blank"):
            Dispute.add_text_evidence(None, "evidence")

    def test_add_text_evidence_empty_evidence_raises_value_exception(self):
        with self.assertRaisesRegex(ValueError, "content cannot be blank"):
            Dispute.add_text_evidence("dispute_id", " ")

    def test_add_text_evidence_sequence_number_not_number_evidence_raises_value_exception(self):
        with self.assertRaisesRegex(ValueError, "sequence_number must be an integer"):
            Dispute.add_text_evidence("dispute_id", { "content": "content", "sequence_number": "a" })

    def test_add_text_evidence_sequence_number_number_and_letter_evidence_raises_value_exception(self):
        with self.assertRaisesRegex(ValueError, "sequence_number must be an integer"):
            Dispute.add_text_evidence("dispute_id", { "content": "content", "sequence_number": "1abc" })

    def test_add_text_evidence_category_is_number_evidence_raises_value_exception(self):
        with self.assertRaisesRegex(ValueError, "category must be a string"):
            Dispute.add_text_evidence("dispute_id", { "content": "content", "category": 5 })

    def test_add_file_evidence_empty_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "dispute with id ' ' not found"):
            Dispute.add_file_evidence(" ", 1)

    def test_add_file_evidence_none_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "dispute with id None not found"):
            Dispute.add_file_evidence(None, 1)

    def test_add_file_evidence_empty_evidence_raises_value_exception(self):
        with self.assertRaisesRegex(ValueError, "document_id cannot be blank"):
            Dispute.add_file_evidence("dispute_id", " ")

    def test_add_file_evidence_none_evidence_raises_value_exception(self):
        with self.assertRaisesRegex(ValueError, "document_id cannot be blank"):
            Dispute.add_file_evidence("dispute_id", None)

    def test_add_file_evidence_categorized_document_id_must_be_a_string(self):
        with self.assertRaisesRegex(ValueError, "category must be a string"):
            Dispute.add_file_evidence("dispute_id", { "document_id": "213", "category": 5 })

    def test_add_file_evidence_empty_categorized_evidence_raises_value_exception(self):
        with self.assertRaisesRegex(ValueError, "document_id cannot be blank"):
            Dispute.add_file_evidence("dispute_id", { "category": "DEVICE_ID" })

    def test_finalize_none_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "dispute with id None not found"):
            Dispute.finalize(None)

    def test_finalize_empty_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "dispute with id ' ' not found"):
            Dispute.finalize(" ")

    def test_finding_none_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "dispute with id None not found"):
            Dispute.find(None)

    def test_finding_empty_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "dispute with id ' ' not found"):
            Dispute.find(" ")

    def test_remove_evidence_empty_dispute_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "evidence with id 'evidence' for dispute with id ' ' not found"):
            Dispute.remove_evidence(" ", "evidence")

    def test_remove_evidence_none_dispute_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "evidence with id 'evidence' for dispute with id None not found"):
            Dispute.remove_evidence(None, "evidence")

    def test_remove_evidence_evidence_none_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "evidence with id None for dispute with id 'dispute_id' not found"):
            Dispute.remove_evidence("dispute_id", None)

    def test_remove_evidence_empty_evidence_id_raises_value_exception(self):
        with self.assertRaisesRegex(NotFoundError, "evidence with id ' ' for dispute with id 'dispute_id' not found"):
            Dispute.remove_evidence("dispute_id", " ")
