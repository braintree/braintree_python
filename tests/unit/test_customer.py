import unittest
from nose.tools import raises
from braintree.customer import Customer
from braintree.exceptions.argument_error import ArgumentError

class TestCustomer(unittest.TestCase):
    @raises(ArgumentError)
    def test_create_raise_exception_with_bad_keys(self):
        Customer.create({"bad_key": "value"})
