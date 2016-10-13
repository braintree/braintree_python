from tests.test_helper import *

class TestUsBankAccount(unittest.TestCase):
    def test_find_returns_us_bank_account(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce()
        })
        self.assertTrue(result.is_success)

        found_account = UsBankAccount.find(result.payment_method.token)
        self.assertEqual(found_account.routing_number, "123456789")
        self.assertEqual(found_account.last_4, "1234")
        self.assertEqual(found_account.account_type, "checking")
        self.assertEqual(found_account.account_description, "PayPal Checking - 1234")
        self.assertEqual(found_account.account_holder_name, "Dan Schulman")

    def test_find_does_not_return_invalid_us_bank_account(self):
        self.assertRaises(NotFoundError, UsBankAccount.find, TestHelper.generate_invalid_us_bank_account_nonce())

    def test_sale_transacts_us_bank_account(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce()
        })
        self.assertTrue(result.is_success)

        params = {
            "amount": TransactionAmounts.Authorize,
            "merchant_account_id": "us_bank_merchant_account",
        }
        result = UsBankAccount.sale(result.payment_method.token, params)

        self.assertTrue(result.is_success)
        self.assertEqual(result.transaction.us_bank_account.routing_number, "123456789")
        self.assertEqual(result.transaction.us_bank_account.last_4, "1234")
        self.assertEqual(result.transaction.us_bank_account.account_type, "checking")
        self.assertEqual(result.transaction.us_bank_account.account_description, "PayPal Checking - 1234")
        self.assertEqual(result.transaction.us_bank_account.account_holder_name, "Dan Schulman")


