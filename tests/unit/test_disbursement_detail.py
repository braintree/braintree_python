from tests.test_helper import *
from braintree.disbursement_detail import DisbursementDetail

class TestDisbursementDetail(unittest.TestCase):
    def test_is_valid_true(self):
        detail_hash = {
            'settlement_amount': '27.00',
            'settlement_currency_iso_code': 'USD',
            'settlement_currency_exchange_rate': '1',
            'disbursed_at': datetime(2013, 4, 11, 0, 0, 0),
            'disbursement_date': date(2013, 4, 10),
            'funds_held': False
        }
        disbursement_details = DisbursementDetail(detail_hash)
        self.assertTrue(disbursement_details.is_valid)

    def test_is_valid_false(self):
        detail_hash = {
            'settlement_amount': None,
            'settlement_currency_iso_code': None,
            'settlement_currency_exchange_rate': None,
            'disbursed_at': None,
            'disbursement_date': None,
            'funds_held': None
        }
        disbursement_details = DisbursementDetail(detail_hash)
        self.assertEqual(False, disbursement_details.is_valid)
