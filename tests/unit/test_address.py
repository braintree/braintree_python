import unittest
from nose.tools import raises
from braintree.address import Address

class TestAddress(unittest.TestCase):
    @raises(KeyError)
    def test_create_raise_exception_with_bad_keys(self):
        Address.create({"customer_id": "12345", "bad_key": "value"})
