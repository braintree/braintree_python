import unittest
from braintree.transaction import Transaction

class TestTransaction(unittest.TestCase):
    def test_sale_raises_exception_with_bad_keys(self):
        try:
            Transaction.sale({"bad_key": "value"})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_sale_raises_exception_with_nested_bad_keys(self):
        try:
            Transaction.sale({"credit_card": {"bad_key": "value"}})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: credit_card[bad_key]'", str(e))
