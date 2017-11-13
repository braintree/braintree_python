from tests.test_helper import *

class TestDisputeSearch(unittest.TestCase):
    def test_advanced_search_no_results(self):
        collection = Dispute.search([
            DisputeSearch.id == "non_existent_dispute"
        ])

        disputes = [dispute for dispute in collection.disputes.items]
        self.assertEquals(0, len(disputes))

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
        self.assertEquals(2, len(disputes))

    def test_advanced_search_returns_disputes_by_date_range(self):
        collection = Dispute.search([
            DisputeSearch.received_date.between("03/03/2014", "03/05/2014")
        ])

        disputes = [dispute for dispute in collection.disputes.items]
        self.assertEquals(1, len(disputes))

        self.assertEquals(disputes[0].received_date, date(2014, 3, 4))
    
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
