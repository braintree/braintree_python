from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers

class TestDisputeSearch(unittest.TestCase):
    def create_sample_disputed_transaction(self):
        customer = Customer.create({
            "first_name": "Jen",
            "last_name": "Smith",
            "company": "Braintree",
            "email": "jen@example.com",
            "phone": "312.555.1234",
            "fax": "614.555.5678",
            "website": "www.example.com",
        }).customer

        return Transaction.sale({
            "amount": "100.00",
            "credit_card": {
                "number": CreditCardNumbers.Disputes.Chargeback,
                "expiration_date": "12/2019",
            },
            "customer_id": customer.id,
            "merchant_account_id": "14LaddersLLC_instant",
            "options": {
                "submit_for_settlement": True,
            },
        }).transaction

    def test_advanced_search_no_results(self):
        collection = Dispute.search([
            DisputeSearch.id == "non_existent_dispute"
        ])

        disputes = [dispute for dispute in collection.disputes.items]
        self.assertEquals(0, len(disputes))

    def test_advanced_search_returns_single_dispute_by_customer_id(self):
        transaction = self.create_sample_disputed_transaction()

        collection = Dispute.search([
            DisputeSearch.customer_id == transaction.customer_details.id
        ])

        disputes = [dispute for dispute in collection.disputes.items]
        self.assertEquals(1, len(disputes))

        dispute = disputes[0]

        self.assertEquals(dispute.id, transaction.disputes[0].id)
        self.assertEquals(dispute.status, Dispute.Status.Open)

    def test_advanced_search_returns_single_dispute_by_id(self):
        collection = Dispute.search([
            DisputeSearch.id == "open_dispute"
        ])

        disputes = [dispute for dispute in collection.disputes.items]
        self.assertEquals(1, len(disputes))

        dispute = disputes[0]

        self.assertEquals(dispute.id, "open_dispute")
        self.assertEquals(dispute.status, Dispute.Status.Open)

    def test_advanced_search_returns_disputes_by_multiple_reasons(self):
        collection = Dispute.search([
            DisputeSearch.reason.in_list([
                braintree.Dispute.Reason.ProductUnsatisfactory,
                braintree.Dispute.Reason.Retrieval
            ])
        ])

        disputes = [dispute for dispute in collection.disputes.items]
        self.assertGreaterEqual(len(disputes), 2)

    def test_advanced_search_returns_disputes_by_chargeback_protection_level(self):
            collection = Dispute.search([
                DisputeSearch.chargeback_protection_level.in_list([
                    braintree.Dispute.ChargebackProtectionLevel.Effortless,
                ])
            ])

            disputes = [dispute for dispute in collection.disputes.items]
            self.assertEqual(len(disputes) > 0, True)

            for dispute in disputes:
                self.assertEqual(dispute.reason, braintree.Dispute.Reason.Fraud)
                # NEXT_MAJOR_VERSION Remove this assertion when chargeback_protection_level is removed from the SDK
                self.assertEqual(dispute.chargeback_protection_level, braintree.Dispute.ChargebackProtectionLevel.Effortless)
                self.assertEqual(dispute.protection_level, braintree.Dispute.ProtectionLevel.EffortlessCBP)

    def test_advanced_search_returns_disputes_by_pre_dispute_program(self):
            collection = Dispute.search([
                DisputeSearch.pre_dispute_program.in_list([
                    braintree.Dispute.PreDisputeProgram.VisaRdr,
                ])
            ])

            disputes = [dispute for dispute in collection.disputes.items]
            self.assertEqual(len(disputes), 1)
            self.assertEqual(disputes[0].pre_dispute_program, braintree.Dispute.PreDisputeProgram.VisaRdr)

    def test_advanced_search_returns_disputes_with_no_pre_dispute_program(self):
            collection = Dispute.search([
                DisputeSearch.pre_dispute_program == braintree.Dispute.PreDisputeProgram.NONE
            ])

            disputes = [dispute for dispute in collection.disputes.items]
            pre_dispute_programs = set([dispute.pre_dispute_program for dispute in disputes])

            self.assertGreater(len(disputes), 1)
            self.assertEqual(len(pre_dispute_programs), 1)
            self.assertIn(braintree.Dispute.PreDisputeProgram.NONE, pre_dispute_programs)

    def test_advanced_search_returns_disputes_by_date_range(self):
        collection = Dispute.search([
            DisputeSearch.received_date.between("03/03/2014", "03/05/2014")
        ])

        disputes = [dispute for dispute in collection.disputes.items]
        self.assertGreaterEqual(len(disputes), 1)

        self.assertEquals(disputes[0].received_date, date(2014, 3, 4))

    def test_advanced_search_returns_disputes_by_disbursement_date_range(self):
        transaction = self.create_sample_disputed_transaction()
        disbursement_date = transaction.disputes[0].status_history[0].disbursement_date

        collection = Dispute.search([
            DisputeSearch.disbursement_date.between(disbursement_date, disbursement_date)
        ])

        disputes = [dispute for dispute in collection.disputes.items]
        self.assertGreaterEqual(len(disputes), 1)

        self.assertEquals(disputes[0].status_history[0].disbursement_date, disbursement_date)

    def test_advanced_search_returns_disputes_by_effective_date_range(self):
        transaction = self.create_sample_disputed_transaction()
        effective_date = transaction.disputes[0].status_history[0].effective_date

        collection = Dispute.search([
            DisputeSearch.effective_date.between(effective_date, effective_date)
        ])

        disputes = [dispute for dispute in collection.disputes.items]
        self.assertGreaterEqual(len(disputes), 1)

        self.assertEquals(disputes[0].status_history[0].effective_date, effective_date)

    def test_advanced_search_returns_disputes_by_amount_and_status(self):
        collection = Dispute.search([
            DisputeSearch.amount_disputed.between("1.00", "100.00"),
            DisputeSearch.id == "open_dispute"
        ])

        disputes = [dispute for dispute in collection.disputes.items]
        self.assertEquals(1, len(disputes))

    def test_advanced_search_can_take_one_criteria(self):
        collection = Dispute.search(
            DisputeSearch.id == "non_existent_dispute"
        )

        disputes = [dispute for dispute in collection.disputes.items]
        self.assertEquals(0, len(disputes))
