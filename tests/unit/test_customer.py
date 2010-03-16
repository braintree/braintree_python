import unittest
from nose.tools import raises
from braintree.customer import Customer

class TestCustomer(unittest.TestCase):
    @raises(KeyError)
    def test_create_raise_exception_with_bad_keys(self):
        Customer.create({"bad_key": "value"})

    @raises(KeyError)
    def test_create_raise_exception_with_bad_nested_keys(self):
        Customer.create({"credit_card": {"bad_key": "value"}})
