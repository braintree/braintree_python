from tests.test_helper import *
from datetime import datetime
from datetime import date

class TestTransaction(unittest.TestCase):
    def test_clone_transaction_raises_exception_with_bad_keys(self):
        try:
            Transaction.clone_transaction("an id", {"bad_key": "value"})
            self.assertTrue(False)
        except KeyError, e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_sale_raises_exception_with_bad_keys(self):
        try:
            Transaction.sale({"bad_key": "value"})
            self.assertTrue(False)
        except KeyError, e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_sale_raises_exception_with_nested_bad_keys(self):
        try:
            Transaction.sale({"credit_card": {"bad_key": "value"}})
            self.assertTrue(False)
        except KeyError, e:
            self.assertEquals("'Invalid keys: credit_card[bad_key]'", str(e))

    def test_tr_data_for_sale_raises_error_with_bad_keys(self):
        try:
            Transaction.tr_data_for_sale({"bad_key": "value"}, "http://example.com")
            self.assertTrue(False)
        except KeyError, e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_finding_empty_id_raises_not_found_exception(self):
        try:
            Transaction.find(" ")
            self.assertTrue(False)
        except NotFoundError, e:
            self.assertTrue(True)

    def test_constructor_includes_deposit_information(self):
        attributes = {
            'amount': '27.00',
            'tax_amount': '1.00',
            'customer_id': '4096',
            'merchant_account_id': '8192',
            'order_id': '106601',
            'channel': '101',
            'payment_method_token': 'sometoken',
            'purchase_order_number': '20202',
            'recurring': 'False',
            'deposit_details': {
                'settlement_amount': '27.00',
                'settlement_currency_iso_code': 'USD',
                'settlement_currency_exchange_rate': '1',
                'disbursed_at': datetime(2013, 4, 11, 0, 0, 0),
                'deposit_date': date(2013, 4, 10),
                'funds_held': False
            }
        }

        tran = Transaction(None, attributes)

        self.assertEquals(tran.deposit_details.settlement_amount, Decimal('27.00'))
        self.assertEquals(tran.deposit_details.settlement_currency_iso_code, 'USD')
        self.assertEquals(tran.deposit_details.settlement_currency_exchange_rate, Decimal('1'))
        self.assertEquals(tran.deposit_details.disbursed_at, datetime(2013, 4, 11, 0, 0, 0))
        self.assertEquals(tran.deposit_details.deposit_date, date(2013, 4, 10))
        self.assertEquals(tran.deposit_details.funds_held, False)
        self.assertEquals(tran.is_deposited, True)

    def test_is_deposited_false(self):
        attributes = {
            'amount': '27.00',
            'tax_amount': '1.00',
            'customer_id': '4096',
            'merchant_account_id': '8192',
            'order_id': '106601',
            'channel': '101',
            'payment_method_token': 'sometoken',
            'purchase_order_number': '20202',
            'recurring': 'False',
            'deposit_details': {
                'settlement_amount': None,
                'settlement_currency_iso_code': None,
                'settlement_currency_exchange_rate': None,
                'disbursed_at': None,
                'deposit_date': None,
                'funds_held': None,
            }
        }

        tran = Transaction(None, attributes)

        self.assertEquals(tran.is_deposited, False)
