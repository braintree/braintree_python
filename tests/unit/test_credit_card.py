import unittest
from nose.tools import raises
from braintree.credit_card import CreditCard

class TestCreditCard(unittest.TestCase):
    @raises(KeyError)
    def test_create_raises_exception_with_bad_keys(self):
        CreditCard.create({"bad_key": "value"})

    @raises(KeyError)
    def test_update_raises_exception_with_bad_keys(self):
        CreditCard.update("token", {"bad_key": "value"})
