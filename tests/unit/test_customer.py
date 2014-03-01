from tests.test_helper import *

class TestCustomer(unittest.TestCase):
    def test_create_raise_exception_with_bad_keys(self):
        try:
            Customer.create({"bad_key": "value"})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_create_raise_exception_with_bad_nested_keys(self):
        try:
            Customer.create({"credit_card": {"bad_key": "value"}})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: credit_card[bad_key]'", str(e))

    def test_update_raise_exception_with_bad_keys(self):
        try:
            Customer.update("id", {"bad_key": "value"})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_update_raise_exception_with_bad_nested_keys(self):
        try:
            Customer.update("id", {"credit_card": {"bad_key": "value"}})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: credit_card[bad_key]'", str(e))

    def test_tr_data_for_create_raises_error_with_bad_keys(self):
        try:
            Customer.tr_data_for_create({"bad_key": "value"}, "http://example.com")
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_tr_data_for_update_raises_error_with_bad_keys(self):
        try:
            Customer.tr_data_for_update({"bad_key": "value"}, "http://example.com")
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_finding_empty_id_raises_not_found_exception(self):
        try:
            Customer.find(" ")
            self.assertTrue(False)
        except NotFoundError as e:
            self.assertTrue(True)
