
from tests.test_helper import *
from braintree.resource import Resource
from braintree.deposit_detail import DepositDetail

class TestDepositDetail(unittest.TestCase):
    def test_is_valid_true(self):
        detail_hash = {
            'settlement_amount': '27.00',
            'settlement_currency_iso_code': 'USD',
            'settlement_currency_exchange_rate': '1',
            'disbursed_at': datetime(2013, 4, 11, 0, 0, 0),
            'deposit_date': date(2013, 4, 10),
            'funds_held': False
        }
        deposit_details = DepositDetail(detail_hash)
        self.assertTrue(deposit_details.is_valid)

    def test_is_valid_false(self):
        detail_hash = {
            'settlement_amount': None,
            'settlement_currency_iso_code': None,
            'settlement_currency_exchange_rate': None,
            'disbursed_at': None,
            'deposit_date': None,
            'funds_held': None
        }
        deposit_details = DepositDetail(detail_hash)
        self.assertEquals(False, deposit_details.is_valid)

