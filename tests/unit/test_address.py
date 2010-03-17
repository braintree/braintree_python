import unittest
from nose.tools import raises
from braintree.address import Address

class TestAddress(unittest.TestCase):
    @raises(KeyError)
    def test_create_raise_exception_with_bad_keys(self):
        Address.create({"customer_id": "12345", "bad_key": "value"})

    @raises(KeyError)
    def test_create_raises_error_if_no_customer_id_given(self):
        Address.create({"country_name": "United States of America"})

    @raises(KeyError)
    def test_create_raises_key_error_if_given_invalid_customer_id(self):
        Address.create({"customer_id": "!@#$%"})
