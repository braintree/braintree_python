from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers
from datetime import datetime
from datetime import date
if sys.version_info[0] == 2:
    from mock import MagicMock
else:
    from unittest.mock import MagicMock

class TestTransaction(unittest.TestCase):
    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_clone_transaction_raises_exception_with_bad_keys(self):
        Transaction.clone_transaction("an id", {"bad_key": "value"})

    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_sale_raises_exception_with_bad_keys(self):
        Transaction.sale({"bad_key": "value"})

    @raises_with_regexp(KeyError, "'Invalid keys: credit_card\[bad_key\]'")
    def test_sale_raises_exception_with_nested_bad_keys(self):
        Transaction.sale({"credit_card": {"bad_key": "value"}})

    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_tr_data_for_sale_raises_error_with_bad_keys(self):
        Transaction.tr_data_for_sale({"bad_key": "value"}, "http://example.com")

    @raises(NotFoundError)
    def test_finding_empty_id_raises_not_found_exception(self):
        Transaction.find(" ")

    @raises(NotFoundError)
    def test_finding_none_raises_not_found_exception(self):
        Transaction.find(None)

    def test_constructor_includes_disbursement_information(self):
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
            'disbursement_details': {
                'settlement_amount': '27.00',
                'settlement_currency_iso_code': 'USD',
                'settlement_currency_exchange_rate': '1',
                'disbursement_date': date(2013, 4, 10),
                'funds_held': False
            }
        }

        transaction = Transaction(None, attributes)

        self.assertEqual(transaction.disbursement_details.settlement_amount, Decimal('27.00'))
        self.assertEqual(transaction.disbursement_details.settlement_currency_iso_code, 'USD')
        self.assertEqual(transaction.disbursement_details.settlement_currency_exchange_rate, Decimal('1'))
        self.assertEqual(transaction.disbursement_details.disbursement_date, date(2013, 4, 10))
        self.assertEqual(transaction.disbursement_details.funds_held, False)
        self.assertEqual(transaction.is_disbursed, True)

    def test_transaction_handles_nil_risk_data(self):
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
        }

        transaction = Transaction(None, attributes)

        self.assertEqual(transaction.risk_data, None)

    def test_is_disbursed_false(self):
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
            'disbursement_details': {
                'settlement_amount': None,
                'settlement_currency_iso_code': None,
                'settlement_currency_exchange_rate': None,
                'disbursement_date': None,
                'funds_held': None,
            }
        }

        transaction = Transaction(None, attributes)

        self.assertEqual(transaction.is_disbursed, False)

    def test_sale_with_skip_advanced_fraud_checking_value_as_true(self):
        attributes = {
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009"
            },
            "options": {
                "skip_advanced_fraud_checking": True
            }
        }

        transaction_gateway = self.setup_transaction_gateway_and_mock_post()
        transaction_gateway.sale(attributes)
        transaction_param = transaction_gateway._post.call_args[0][1]
        self.assertTrue(transaction_param['transaction']['options']['skip_advanced_fraud_checking'])

    def test_sale_with_skip_advanced_fraud_checking_value_as_false(self):
        attributes = {
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009"
            },
            "options": {
                "skip_advanced_fraud_checking": False
            }
        }

        transaction_gateway = self.setup_transaction_gateway_and_mock_post()
        transaction_gateway.sale(attributes)
        transaction_param = transaction_gateway._post.call_args[0][1]
        self.assertFalse(transaction_param['transaction']['options']['skip_advanced_fraud_checking'])

    def test_sale_without_skip_advanced_fraud_checking_value_option(self):
        attributes = {
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009"
            },
            "options": {
                "submit_for_settlement": True
            }
        }

        transaction_gateway = self.setup_transaction_gateway_and_mock_post()
        transaction_gateway.sale(attributes)
        transaction_param = transaction_gateway._post.call_args[0][1]
        self.assertTrue('skip_advanced_fraud_checking' not in transaction_param['transaction']['options'])

    def setup_transaction_gateway_and_mock_post(self):
        transaction_gateway = TransactionGateway(BraintreeGateway(None))
        transaction_gateway._post = MagicMock(name='config.http.post')
        return transaction_gateway
