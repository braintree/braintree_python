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

        self.assertTrue(result.is_success)

        transaction = result.transaction
        TestHelper.settle_transaction(transaction.id)

        result = SettlementBatchSummary.generate(TestHelper.now_in_eastern())
        self.assertTrue(result.is_success)

        visa_records = [row for row in result.settlement_batch_summary.records if row['card_type'] == 'Visa'][0]
        self.assertTrue(int(visa_records['count']) >= 1)
        self.assertTrue(float(visa_records['amount_settled']) >= float(TransactionAmounts.Authorize))

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

        transaction = result.transaction
        TestHelper.settle_transaction(transaction.id)

        result = SettlementBatchSummary.generate(TestHelper.now_in_eastern(), 'store_me')
        self.assertTrue(result.is_success)

        self.assertTrue('store_me' in result.settlement_batch_summary.records[0])
