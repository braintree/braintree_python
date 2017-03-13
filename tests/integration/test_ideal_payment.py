from braintree.transaction_amounts import TransactionAmounts
from decimal import Decimal
from tests.test_helper import *

class TestIdealPayment(unittest.TestCase):
    def test_sale_transacts_ideal_payment(self):
        valid_nonce = TestHelper.generate_valid_ideal_payment_nonce()
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "order_id": "ABC123",
            "merchant_account_id": "ideal_merchant_account",
            "payment_method_nonce": valid_nonce,
            "options": {
                "submit_for_settlement": True,
            },
        })

        self.assertTrue(result.is_success)

        self.assertRegexpMatches(result.transaction.id, r'^\w{6,}$')
        self.assertEqual(result.transaction.type, "sale")
        self.assertEqual(result.transaction.payment_instrument_type, PaymentInstrumentType.IdealPayment)
        self.assertEqual(result.transaction.amount, Decimal(TransactionAmounts.Authorize))
        self.assertEqual(result.transaction.status, Transaction.Status.Settled)
        self.assertRegexpMatches(result.transaction.ideal_payment_details.ideal_payment_id, r"^idealpayment_\w{6,}")
        self.assertRegexpMatches(result.transaction.ideal_payment_details.ideal_transaction_id, r"^\d{16,}$")
        self.assertEqual(result.transaction.ideal_payment_details.image_url[:8], 'https://')
        self.assertNotEqual(result.transaction.ideal_payment_details.masked_iban, None)
        self.assertNotEqual(result.transaction.ideal_payment_details.bic, None)

    def test_failed_sale_non_complete_ideal_payment(self):
        non_complete_nonce = TestHelper.generate_valid_ideal_payment_nonce("3.00")
        result = Transaction.sale({
            "amount": "3.00",
            "order_id": "ABC123",
            "merchant_account_id": "ideal_merchant_account",
            "payment_method_nonce": non_complete_nonce,
            "options": {
                "submit_for_settlement": True,
            },
        })
        error_codes = [
            error.code for error in result.errors.for_object("transaction").on("payment_method_nonce")
        ]

        self.assertFalse(result.is_success)
        self.assertTrue(ErrorCodes.Transaction.IdealPaymentNotComplete in error_codes)
