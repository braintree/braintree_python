import unittest
from braintree.address import Address

class TestAddress(unittest.TestCase):
    def test_create_raise_exception_with_bad_keys(self):
        try:
            Address.create({"customer_id": "12345", "bad_key": "value"})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'bad_key is not an allowed key'", str(e))

    def test_create_raises_error_if_no_customer_id_given(self):
        try:
            Address.create({"country_name": "United States of America"})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'customer_id must be provided'", str(e))

    def test_create_raises_key_error_if_given_invalid_customer_id(self):
        try:
            Address.create({"customer_id": "!@#$%"})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'customer_id contains invalid characters'", str(e))

    def test_update_raise_exception_with_bad_keys(self):
        try:
            Address.update("customer_id", "address_id", {"bad_key": "value"})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'bad_key is not an allowed key'", str(e))

