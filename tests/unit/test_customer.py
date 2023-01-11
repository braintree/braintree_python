from tests.test_helper import *

class TestCustomer(unittest.TestCase):
    def test_create_raise_exception_with_bad_keys(self):
        with self.assertRaisesRegex(KeyError, "'Invalid keys: bad_key'"):
            Customer.create({"bad_key": "value"})

    def test_create_raise_exception_with_bad_nested_keys(self):
        with self.assertRaisesRegex(KeyError, "'Invalid keys: credit_card\[bad_key\]'"):
            Customer.create({"credit_card": {"bad_key": "value"}})

    def test_update_raise_exception_with_bad_keys(self):
        with self.assertRaisesRegex(KeyError, "'Invalid keys: bad_key'"):
            Customer.update("id", {"bad_key": "value"})

    def test_update_raise_exception_with_bad_nested_keys(self):
        with self.assertRaisesRegex(KeyError, "'Invalid keys: credit_card\[bad_key\]'"):
            Customer.update("id", {"credit_card": {"bad_key": "value"}})

    def test_finding_empty_id_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            Customer.find(" ")

    def test_finding_none_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            Customer.find(None)

    def test_initialize_sets_paypal_accounts(self):
        customer = Customer("gateway", {
            "paypal_accounts": [
                {"token": "token1"},
                {"token": "token2"}
            ],
            "sepa_debit_accounts": [
                {"token": "sdd1"},
                {"token": "sdd2"}
            ]
        })

        self.assertEqual(2, len(customer.paypal_accounts))
        self.assertEqual("token1", customer.paypal_accounts[0].token)
        self.assertEqual("token2", customer.paypal_accounts[1].token)
        self.assertEqual(2, len(customer.sepa_direct_debit_accounts))
        self.assertEqual("sdd1", customer.sepa_direct_debit_accounts[0].token)
        self.assertEqual("sdd2", customer.sepa_direct_debit_accounts[1].token)
