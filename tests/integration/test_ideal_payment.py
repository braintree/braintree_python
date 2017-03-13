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
