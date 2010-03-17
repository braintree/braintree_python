import unittest
from braintree.customer import Customer

class TestCustomer(unittest.TestCase):
    def test_create_raise_exception_with_bad_keys(self):
        try:
            Customer.create({"bad_key": "value"})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'bad_key is not an allowed key'", str(e))

    def test_create_raise_exception_with_bad_nested_keys(self):
        try:
            Customer.create({"credit_card": {"bad_key": "value"}})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'bad_key is not an allowed key'", str(e))
