import unittest
from braintree.customer import Customer

class TestCustomer(unittest.TestCase):
    def test_create_raise_exception_with_bad_keys(self):
        try:
            Customer.create({"bad_key": "value"})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_create_raise_exception_with_bad_nested_keys(self):
        try:
            Customer.create({"credit_card": {"bad_key": "value"}})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: credit_card[bad_key]'", str(e))
