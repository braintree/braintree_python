from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers
from braintree.meta_checkout_card import MetaCheckoutCard
from braintree.meta_checkout_token import MetaCheckoutToken
from datetime import datetime
from datetime import date
from braintree.authorization_adjustment import AuthorizationAdjustment
from unittest.mock import MagicMock

class TestTransaction(unittest.TestCase):
    def test_clone_transaction_raises_exception_with_bad_keys(self):
        with self.assertRaisesRegex(KeyError, "'Invalid keys: bad_key'"):
            Transaction.clone_transaction("an id", {"bad_key": "value"})

    def test_sale_raises_exception_with_bad_keys(self):
        with self.assertRaisesRegex(KeyError, "'Invalid keys: bad_key'"):
            Transaction.sale({"bad_key": "value"})

    def test_sale_raises_exception_with_nested_bad_keys(self):
        with self.assertRaisesRegex(KeyError, "'Invalid keys: credit_card\[bad_key\]'"):
            Transaction.sale({"credit_card": {"bad_key": "value"}})

    def test_finding_empty_id_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            Transaction.find(" ")

    def test_finding_none_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
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

    def test_constructor_includes_sepa_direct_debit_return_code(self):
        attributes = {
            'amount': '27.00',
            'sepa_direct_debit_return_code': 'AM04'
        }

        transaction = Transaction(None, attributes)

        self.assertEqual(transaction.sepa_direct_debit_return_code, 'AM04')

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

    def test_sale_with_external_network_token_option(self):
        attributes = {
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
                "network_tokenization_attributes": {
                    "cryptogram": "/wAAAAAAAcb8AlGUF/1JQEkAAAA=",
                    "ecommerce_indicator": "45310020105",
                    "token_requestor_id" : "05"
                }
            }
        }

        transaction_gateway = self.setup_transaction_gateway_and_mock_post()
        transaction_gateway.sale(attributes)
        transaction_param = transaction_gateway._post.call_args[0][1]
        self.assertTrue('network_tokenization_attributes' in transaction_param['transaction']['credit_card'])
        self.assertEqual(transaction_param['transaction']['credit_card']['network_tokenization_attributes']['cryptogram'], "/wAAAAAAAcb8AlGUF/1JQEkAAAA=")
        self.assertEqual(transaction_param['transaction']['credit_card']['network_tokenization_attributes']['ecommerce_indicator'], "45310020105")
        self.assertEqual(transaction_param['transaction']['credit_card']['network_tokenization_attributes']['token_requestor_id'], "05")

    def setup_transaction_gateway_and_mock_post(self):
        transaction_gateway = TransactionGateway(BraintreeGateway(None))
        transaction_gateway._post = MagicMock(name='config.http.post')
        return transaction_gateway

    def test_constructor_doesnt_includes_auth_adjustments(self):
        attributes = {
            'amount': '27.00',
            'customer_id': '4096',
            'merchant_account_id': '8192',
            'payment_method_token': 'sometoken',
            'purchase_order_number': '20202',
            'recurring': 'False',
            'tax_amount': '1.00',
        }

        transaction = Transaction(None, attributes)
        self.assertFalse(hasattr(transaction, 'authorization_adjustments'))

    def test_constructor_includes_auth_adjustments(self):
        attributes = {
            'amount': '27.00',
            'customer_id': '4096',
            'merchant_account_id': '8192',
            'payment_method_token': 'sometoken',
            'purchase_order_number': '20202',
            'recurring': 'False',
            'tax_amount': '1.00',
            'authorization_adjustments': [{
                "amount": "20.00",
                "timestamp": datetime(2017, 7, 12, 1, 2, 3),
                "success": True,
                "processor_response_code": "1000",
                "processor_response_text": "Approved",
            }],
        }

        transaction = Transaction(None, attributes)
        transaction_adjustment = transaction.authorization_adjustments[0]
        self.assertEqual(transaction_adjustment.amount, Decimal("20.00"))
        self.assertEqual(transaction_adjustment.timestamp, datetime(2017, 7, 12, 1, 2, 3))
        self.assertEqual(transaction_adjustment.success, True)
        self.assertEqual(transaction_adjustment.processor_response_code, "1000")
        self.assertEqual(transaction_adjustment.processor_response_text, "Approved")

    def test_constructor_parses_shipments_into_packages(self):
        attributes = {
            'amount': '27.00',
            'customer_id': '4096',
            'merchant_account_id': '8192',
            'payment_method_token': 'sometoken',
            'purchase_order_number': '20202',
            'recurring': 'False',
            'tax_amount': '1.00',
            'shipments': [
                 {
                    'id': 'id1',
                    'carrier': 'UPS',
                    'tracking_number': 'tracking_number_1',
                    # NEXT_MAJOR_VERSION remove paypal_tracking_id
                    'paypal_tracking_id': 'pp_tracking_number_1',
                    'paypal_tracker_id': 'pp_tracker_id_1',
                },
                {
                    'id': 'id2',
                    'carrier': 'FEDEX',
                    'tracking_number': 'tracking_number_2',
                    # NEXT_MAJOR_VERSION remove paypal_tracking_id
                    'paypal_tracking_id': 'pp_tracking_number_2',
                    'paypal_tracker_id': 'pp_tracker_id_2',
                },
            ],
        }

        transaction = Transaction(None, attributes)
        package_detail_1 = transaction.packages[0]
        self.assertEqual(package_detail_1.id, "id1")
        self.assertEqual(package_detail_1.carrier, "UPS")
        self.assertEqual(package_detail_1.tracking_number, "tracking_number_1")
        # NEXT_MAJOR_VERSION remove paypal_tracking_id assertions.
        self.assertEqual(package_detail_1.paypal_tracking_id, "pp_tracking_number_1")
        self.assertEqual(package_detail_1.paypal_tracker_id, "pp_tracker_id_1")

        package_detail_2 = transaction.packages[1]
        self.assertEqual(package_detail_2.id, "id2")
        self.assertEqual(package_detail_2.carrier, "FEDEX")
        self.assertEqual(package_detail_2.tracking_number, "tracking_number_2")
        # NEXT_MAJOR_VERSION remove paypal_tracking_id assertions.
        self.assertEqual(package_detail_2.paypal_tracking_id, "pp_tracking_number_2")
        self.assertEqual(package_detail_2.paypal_tracker_id, "pp_tracker_id_2")

    def test_constructor_works_with_empty_shipments_list(self):
        attributes = {
            'amount': '27.00',
            'customer_id': '4096',
            'merchant_account_id': '8192',
            'payment_method_token': 'sometoken',
            'purchase_order_number': '20202',
            'recurring': 'False',
            'tax_amount': '1.00',
            'shipments': [],
        }

        transaction = Transaction(None, attributes)
        self.assertEqual(len(transaction.packages), 0)

    def test_constructor_includes_network_transaction_id_and_response_code_and_response_text(self):
        attributes = {
            'amount': '27.00',
            'tax_amount': '1.00',
            'network_transaction_id': '123456789012345',
            'network_response_code': '00',
            'network_response_text': 'Successful approval/completion or V.I.P. PIN verification is successful'
        }

        transaction = Transaction(None, attributes)
        self.assertEqual(transaction.network_transaction_id, "123456789012345")
        self.assertEqual(transaction.network_response_code, "00")
        self.assertEqual(transaction.network_response_text, "Successful approval/completion or V.I.P. PIN verification is successful")

    def test_constructor_includes_installment_count(self):
        attributes = {
            'amount': '27.00',
            'tax_amount': '1.00',
            'installments': {
                'count': 4
            }
        }

        transaction = Transaction(None, attributes)
        self.assertEqual(transaction.installments["count"], 4)

    def test_gateway_rejection_reason_for_excessive_retry(self):
        attributes = {
            'amount': '27.00',
            'gateway_rejection_reason': 'excessive_retry'
        }

        transaction = Transaction(None, attributes)
        self.assertEqual(transaction.gateway_rejection_reason, braintree.Transaction.GatewayRejectionReason.ExcessiveRetry)

    def test_merchant_advice_code(self):
        attributes = {
            'amount': TransactionAmounts.Decline,
            'merchant_advice_code': "01",
            'merchant_advice_code_text': "New account information available"
        }

        transaction = Transaction(None, attributes)
        self.assertEqual(transaction.merchant_advice_code, "01")
        self.assertEqual(transaction.merchant_advice_code_text, "New account information available")

    def test_retry_ids_and_retried_transaction_id(self):
        attributes = {
            'amount': TransactionAmounts.Decline,
            'retry_ids': ['retry_id_1','retry_id2'],
            'retried_transaction_id': '12345',
            'retried': True
        }

        transaction = Transaction(None, attributes)
        self.assertEqual(transaction.retry_ids, ['retry_id_1','retry_id2'])
        self.assertEqual(transaction.retried_transaction_id, "12345")
        self.assertTrue(transaction.retried)

    def test_debit_network(self):
        attributes = {
            'amount': '27.00',
            'debit_network' : CreditCard.DebitNetwork.Star
        }
        transaction = Transaction(None, attributes)
        self.assertEqual(transaction.debit_network, CreditCard.DebitNetwork.Star)

    def test_transaction_meta_checkout_card_attributes(self):
        attributes = {
            'amount': '420',
            'meta_checkout_card': {}
        }

        transaction = Transaction(None, attributes)
        self.assertIsInstance(transaction.meta_checkout_card_details, MetaCheckoutCard)

    def test_transaction_meta_checkout_token_attributes(self):
        attributes = {
            'amount': '69',
            'meta_checkout_token': {}
        }

        transaction = Transaction(None, attributes)
        self.assertIsInstance(transaction.meta_checkout_token_details, MetaCheckoutToken)

    def test_foreign_retailer(self):
        attributes = {
            'amount': TransactionAmounts.Authorize,
            'foreign_retailer': True,
        }

        transaction = Transaction(None, attributes)
        self.assertTrue(transaction.foreign_retailer)