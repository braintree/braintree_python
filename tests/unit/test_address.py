from tests.test_helper import *

class TestAddress(unittest.TestCase):
    def test_create_raise_exception_with_bad_keys(self):
        with self.assertRaisesRegex(KeyError, "'Invalid keys: bad_key'"):
            Address.create({"customer_id": "12345", "bad_key": "value"})

    def test_create_raises_error_if_no_customer_id_given(self):
        with self.assertRaisesRegex(KeyError, "'customer_id must be provided'"):
            Address.create({"country_name": "United States of America"})

    def test_create_raises_key_error_if_given_invalid_customer_id(self):
        with self.assertRaisesRegex(KeyError, "'customer_id contains invalid characters'"):
            Address.create({"customer_id": "!@#$%"})

    def test_update_raise_exception_with_bad_keys(self):
        with self.assertRaisesRegex(KeyError, "'Invalid keys: bad_key'"):
            Address.update("customer_id", "address_id", {"bad_key": "value"})

    def test_update_raises_key_error_if_given_invalid_customer_id(self):
        with self.assertRaisesRegex(KeyError, "'customer_id contains invalid characters'"):
            Address.update("!@#$%", "foo")

    def test_update_raises_key_error_if_given_invalid_address_id(self):
        with self.assertRaisesRegex(KeyError, "'address_id contains invalid characters'"):
            Address.update("foo", "!@#$%")

    def test_delete_raises_key_error_if_given_invalid_customer_id(self):
        with self.assertRaisesRegex(KeyError, "'customer_id contains invalid characters'"):
            Address.delete("!@#$%", "foo")

    def test_delete_raises_key_error_if_given_invalid_address_id(self):
        with self.assertRaisesRegex(KeyError, "'address_id contains invalid characters'"):
            Address.delete("foo", "!@#$%")

    def test_finding_address_with_empty_customer_id_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            Address.find(" ", "address_id")

    def test_finding_address_with_none_customer_id_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            Address.find(None, "address_id")

    def test_finding_address_with_empty_address_id_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            Address.find("customer_id", " ")

    def test_finding_address_with_none_address_id_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            Address.find("customer_id", None)

    def test_find_raises_key_error_if_given_invalid_customer_id(self):
        with self.assertRaisesRegex(KeyError, "'customer_id contains invalid characters'"):
            Address.find("!@#$%", "foo")

    def test_find_raises_key_error_if_given_invalid_address_id(self):
        with self.assertRaisesRegex(KeyError, "'address_id contains invalid characters'"):
            Address.find("foo", "!@#$%")
