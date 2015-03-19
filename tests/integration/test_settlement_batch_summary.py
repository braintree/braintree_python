from tests.test_helper import *

class TestSettlementBatchSummary(unittest.TestCase):
    possible_gateway_time_zone_offsets = (5,4)

    def test_generate_returns_empty_collection_if_there_is_no_data(self):
        result = SettlementBatchSummary.generate('2011-01-01')

        self.assertTrue(result.is_success)
        self.assertEquals([], result.settlement_batch_summary.records)

    def test_generate_returns_error_if_date_can_not_be_parsed(self):
        result = SettlementBatchSummary.generate('THIS AINT NO DATE')

        self.assertFalse(result.is_success)
        code = result.errors.for_object('settlement_batch_summary').on('settlement_date')[0].code
        self.assertEquals(ErrorCodes.SettlementBatchSummary.SettlementDateIsInvalid, code)

    def test_generate_returns_transactions_settled_on_a_given_day(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": "Sergio Ramos"
            },
            "options": {"submit_for_settlement": True}
        })

        TestHelper.settle_transaction(result.transaction.id)

        succesfully_match_amount_settled = False
        for offset in self.possible_gateway_time_zone_offsets:
            result = SettlementBatchSummary.generate(TestHelper.now_minus_offset(offset))
            self.assertTrue(result.is_success)

            visa_records = [row for row in result.settlement_batch_summary.records if row['card_type'] == 'Visa'][0]
            count = int(visa_records['count'])

            succesfully_match_amount_settled = float(visa_records['amount_settled']) == float(TransactionAmounts.Authorize) * count
            if succesfully_match_amount_settled: break

        self.assertTrue(count >= 1)
        self.assertTrue(succesfully_match_amount_settled)

    def test_generate_can_be_grouped_by_a_custom_field(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": "Sergio Ramos"
            },
            "options": {"submit_for_settlement": True},
            "custom_fields": {
                "store_me": 1
            }
        })

        TestHelper.settle_transaction(result.transaction.id)

        for offset in self.possible_gateway_time_zone_offsets:
            result = SettlementBatchSummary.generate(TestHelper.now_minus_offset(offset), 'store_me')
            self.assertTrue(result.is_success)

            if len(result.settlement_batch_summary.records) > 0: break

        self.assertTrue('store_me' in result.settlement_batch_summary.records[0])
