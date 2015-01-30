from tests.test_helper import *

from braintree.test.nonces import Nonces
from braintree.exceptions.not_found_error import NotFoundError

class TestCoinbase(unittest.TestCase):

    def _assert_valid_coinbase_account(self, account):
        for attr in ["user_name", "user_email", "user_id"]:
            self.assertIsNotNone(getattr(account, attr))

    def test_customer(self):
        result = Customer.create({"payment_method_nonce": Nonces.Coinbase})
        customer = Customer.find(result.customer.id)
        account = customer.coinbase_accounts[0]
        self.assertIsNotNone(account)
        self._assert_valid_coinbase_account(account)

    def test_vault(self):
        result = Customer.create()
        result = PaymentMethod.create({
            "customer_id": result.customer.id,
            "payment_method_nonce": Nonces.Coinbase
        })

        account = result.payment_method
        self._assert_valid_coinbase_account(account)

        PaymentMethod.delete(account.token)

        self.assertRaises(braintree.exceptions.NotFoundError, PaymentMethod.find, account.token)

    def test_transaction(self):
        result = Transaction.sale({"payment_method_nonce": Nonces.Coinbase, "amount": "1.00"})
        account = result.transaction.coinbase_details
        self._assert_valid_coinbase_account(account)
