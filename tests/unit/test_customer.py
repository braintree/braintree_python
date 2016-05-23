from tests.test_helper import *

class TestCustomer(unittest.TestCase):
    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_create_raise_exception_with_bad_keys(self):
        Customer.create({"bad_key": "value"})

    @raises_with_regexp(KeyError, "'Invalid keys: credit_card\[bad_key\]'")
    def test_create_raise_exception_with_bad_nested_keys(self):
        Customer.create({"credit_card": {"bad_key": "value"}})

    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_update_raise_exception_with_bad_keys(self):
        Customer.update("id", {"bad_key": "value"})

    @raises_with_regexp(KeyError, "'Invalid keys: credit_card\[bad_key\]'")
    def test_update_raise_exception_with_bad_nested_keys(self):
        Customer.update("id", {"credit_card": {"bad_key": "value"}})

    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_tr_data_for_create_raises_error_with_bad_keys(self):
        Customer.tr_data_for_create({"bad_key": "value"}, "http://example.com")

    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_tr_data_for_update_raises_error_with_bad_keys(self):
        Customer.tr_data_for_update({"bad_key": "value"}, "http://example.com")

    @raises(NotFoundError)
    def test_finding_empty_id_raises_not_found_exception(self):
        Customer.find(" ")

    @raises(NotFoundError)
    def test_finding_none_raises_not_found_exception(self):
        Customer.find(None)

    def test_initialize_sets_paypal_accounts(self):
        customer = Customer("gateway", {
            "paypal_accounts": [
                {"token": "token1"},
                {"token": "token2"}
            ]
        })

        self.assertEquals(customer.paypal_accounts[0].token, "token1")
        self.assertEquals(customer.paypal_accounts[1].token, "token2")

    def test_initialize_sets_europe_bank_accounts(self):
        customer = Customer("gateway", {
            "europe_bank_accounts": [
                {"token": "token1"},
                {"token": "token2"}
            ]
        })

        self.assertEquals(customer.europe_bank_accounts[0].token, "token1")
        self.assertEquals(customer.europe_bank_accounts[1].token, "token2")
