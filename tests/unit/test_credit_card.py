import unittest
from nose.tools import raises
from braintree.credit_card import CreditCard
from braintree.exceptions.argument_error import ArgumentError

class TestCreditCard(unittest.TestCase):
    @raises(ArgumentError)
    def test_create_raise_exception_with_bad_keys(self):
        CreditCard.create({"bad_key": "value"})
