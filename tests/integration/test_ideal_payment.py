from braintree.transaction_amounts import TransactionAmounts
from braintree.ideal_payment import IdealPayment
from decimal import Decimal
from tests.test_helper import *

class TestIdealPayment(unittest.TestCase):
    def test_creates_transaction_using_ideal_payment_token_and_returns_result_object(self):
        ideal_payment_id = TestHelper.generate_valid_ideal_payment_nonce(amount=TransactionAmounts.Authorize)

        result = IdealPayment.sale(ideal_payment_id, {
            'order_id': 'ABC123',
            'merchant_account_id': 'ideal_merchant_account',
            'amount': TransactionAmounts.Authorize,
        })

        self.assertTrue(result.is_success)
        self.assertEqual(result.transaction.amount, Decimal(TransactionAmounts.Authorize))
        self.assertEqual(result.transaction.type, 'sale')

        ideal_payment_details = result.transaction.ideal_payment_details
        self.assertRegexpMatches(ideal_payment_details.ideal_payment_id, r'^idealpayment_\w{6,}$')
        self.assertRegexpMatches(ideal_payment_details.ideal_transaction_id, r'^\d{16,}$')
        self.assertEqual(ideal_payment_details.image_url[:8], 'https://')
        self.assertNotEqual(ideal_payment_details.masked_iban, None)
        self.assertNotEqual(ideal_payment_details.bic, None)

    def test_doesnt_create_transaction_with_ideal_payment(self):
        result = IdealPayment.sale('invalid_nonce', {
            'merchant_account_id': 'ideal_merchant_account',
            'amount': TransactionAmounts.Authorize,
        })
        self.assertFalse(result.is_success)

    def test_find_ideal_payment_by_id(self):
        ideal_payment_id = TestHelper.generate_valid_ideal_payment_nonce(amount=TransactionAmounts.Authorize)
        ideal_payment = IdealPayment.find(ideal_payment_id)

        self.assertRegexpMatches(ideal_payment.id, r'^idealpayment_\w{6,}$')
        self.assertRegexpMatches(ideal_payment.ideal_transaction_id, r'^\d{16,}$')
        self.assertNotEqual(ideal_payment.currency, None)
        self.assertNotEqual(ideal_payment.amount, None)
        self.assertNotEqual(ideal_payment.status, None)
        self.assertNotEqual(ideal_payment.order_id, None)
        self.assertNotEqual(ideal_payment.issuer, None)
        self.assertEqual(ideal_payment.approval_url[:8], 'https://')
        self.assertNotEqual(ideal_payment.iban_bank_account.account_holder_name, None)
        self.assertNotEqual(ideal_payment.iban_bank_account.bic, None)
        self.assertNotEqual(ideal_payment.iban_bank_account.masked_iban, None)
        self.assertRegexpMatches(ideal_payment.iban_bank_account.iban_account_number_last_4, r'^\d{4}$')
        self.assertNotEqual(ideal_payment.iban_bank_account.iban_country, None)
        self.assertNotEqual(ideal_payment.iban_bank_account.description, None)

    def test_errors_if_ideal_payment_is_not_found(self):
        def find():
            IdealPayment.find('idealpayment_nxyqkq_s654wq_92jr64_mnr4kr_yjz')
        self.assertRaises(NotFoundError, find)
