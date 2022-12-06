from tests.test_helper import *
from braintree.payment_instrument_type import PaymentInstrumentType
from braintree.us_bank_account_verification import UsBankAccountVerification

class TestTransactionWithUsBankAccount(unittest.TestCase):
    def test_nonce_transactions(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "merchant_account_id": TestHelper.us_bank_merchant_account_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce(),
            "options": {
                "submit_for_settlement": True,
                "store_in_vault": True
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual(result.transaction.us_bank_account.routing_number, "021000021")
        self.assertEqual(result.transaction.us_bank_account.last_4, "1234")
        self.assertEqual(result.transaction.us_bank_account.account_type, "checking")
        self.assertEqual(result.transaction.us_bank_account.account_holder_name, "Dan Schulman")
        self.assertTrue(re.match(r".*CHASE.*", result.transaction.us_bank_account.bank_name))
        self.assertEqual(result.transaction.us_bank_account.ach_mandate.text, "cl mandate text")
        self.assertIsInstance(result.transaction.us_bank_account.ach_mandate.accepted_at, datetime)

    def test_nonce_transactions_with_vaulted_token(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "merchant_account_id": TestHelper.us_bank_merchant_account_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce(),
            "options": {
                "submit_for_settlement": True,
                "store_in_vault": True
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual(result.transaction.us_bank_account.routing_number, "021000021")
        self.assertEqual(result.transaction.us_bank_account.last_4, "1234")
        self.assertEqual(result.transaction.us_bank_account.account_type, "checking")
        self.assertEqual(result.transaction.us_bank_account.account_holder_name, "Dan Schulman")
        self.assertTrue(re.match(r".*CHASE.*", result.transaction.us_bank_account.bank_name))
        self.assertEqual(result.transaction.us_bank_account.ach_mandate.text, "cl mandate text")
        self.assertIsInstance(result.transaction.us_bank_account.ach_mandate.accepted_at, datetime)
        token = result.transaction.us_bank_account.token

        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "merchant_account_id": TestHelper.us_bank_merchant_account_id,
            "payment_method_token": token,
            "options": {
                "submit_for_settlement": True,
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual(result.transaction.us_bank_account.routing_number, "021000021")
        self.assertEqual(result.transaction.us_bank_account.last_4, "1234")
        self.assertEqual(result.transaction.us_bank_account.account_type, "checking")
        self.assertEqual(result.transaction.us_bank_account.account_holder_name, "Dan Schulman")
        self.assertTrue(re.match(r".*CHASE.*", result.transaction.us_bank_account.bank_name))
        self.assertEqual(result.transaction.us_bank_account.ach_mandate.text, "cl mandate text")
        self.assertIsInstance(result.transaction.us_bank_account.ach_mandate.accepted_at, datetime)

    def test_token_transactions_not_found(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "merchant_account_id": TestHelper.us_bank_merchant_account_id,
            "payment_method_nonce": TestHelper.generate_invalid_us_bank_account_nonce(),
            "options": {
                "submit_for_settlement": True,
                "store_in_vault": True
            }
        })

        self.assertFalse(result.is_success)
        error_code = result.errors.for_object("transaction").on("payment_method_nonce")[0].code
        self.assertEqual(error_code, ErrorCodes.Transaction.PaymentMethodNonceUnknown)

class TestTransactionWithUsBankAccountCompliantMerchant(unittest.TestCase):
    def setUp(self):
        braintree.Configuration.configure(
            braintree.Environment.Development,
            "integration2_merchant_id",
            "integration2_public_key",
            "integration2_private_key"
        )

    def tearDown(self):
        braintree.Configuration.configure(
            braintree.Environment.Development,
            "integration_merchant_id",
            "integration_public_key",
            "integration_private_key"
        )

    def test_reject_non_plaid_nonce(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "merchant_account_id": "another_us_bank_merchant_account",
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce(),
            "options": {
                "submit_for_settlement": True,
                "store_in_vault": True
            }
        })

        self.assertFalse(result.is_success)
        error_code = result.errors.for_object("transaction").on("payment_method_nonce")[0].code
        self.assertEqual(ErrorCodes.Transaction.UsBankAccountNonceMustBePlaidVerified, error_code)
