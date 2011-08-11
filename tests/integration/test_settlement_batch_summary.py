from tests.test_helper import *

class TestSettlementBatchSummary(unittest.TestCase):
    def test_generate_returns_empty_collection_if_there_is_no_data(self):
        result = SettlementBatchSummary.generate('2011-01-01')

        self.assertTrue(result.is_success)
        self.assertEquals([], result.settlement_batch_summary.records)

    def test_generate_returns_error_if_date_can_not_be_parsed(self):
        result = SettlementBatchSummary.generate('THIS AINT NO DATE')

        self.assertFalse(result.is_success)
        code = result.errors.for_object('settlement_batch_summary').on('settlement_date')[0].code
        self.assertEquals(ErrorCodes.SettlementBatchSummary.SettlementDateIsInvalid, code)
