from tests.test_helper import *

class TestTransaction(unittest.TestCase):
    def test_clone_transaction_raises_exception_with_bad_keys(self):
        try:
            Transaction.clone_transaction("an id", {"bad_key": "value"})
            self.assertTrue(False)
        except KeyError, e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_sale_raises_exception_with_bad_keys(self):
        try:
            Transaction.sale({"bad_key": "value"})
            self.assertTrue(False)
        except KeyError, e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_sale_raises_exception_with_nested_bad_keys(self):
        try:
            Transaction.sale({"credit_card": {"bad_key": "value"}})
            self.assertTrue(False)
        except KeyError, e:
            self.assertEquals("'Invalid keys: credit_card[bad_key]'", str(e))

    def test_tr_data_for_sale_raises_error_with_bad_keys(self):
        try:
            Transaction.tr_data_for_sale({"bad_key": "value"}, "http://example.com")
            self.assertTrue(False)
        except KeyError, e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_finding_empty_id_raises_not_found_exception(self):
        try:
            Transaction.find(" ")
            self.assertTrue(false)
        except NotFoundError, e:
            self.assertIsNotNone(str(e))
