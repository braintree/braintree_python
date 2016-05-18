from tests.test_helper import *

class TestAddress(unittest.TestCase):
    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_create_raise_exception_with_bad_keys(self):
        Address.create({"customer_id": "12345", "bad_key": "value"})

    @raises_with_regexp(KeyError, "'customer_id must be provided'")
    def test_create_raises_error_if_no_customer_id_given(self):
        Address.create({"country_name": "United States of America"})

    @raises_with_regexp(KeyError, "'customer_id contains invalid characters'")
    def test_create_raises_key_error_if_given_invalid_customer_id(self):
        Address.create({"customer_id": "!@#$%"})

    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_update_raise_exception_with_bad_keys(self):
        Address.update("customer_id", "address_id", {"bad_key": "value"})

    @raises(NotFoundError)
    def test_finding_address_with_empty_customer_id_raises_not_found_exception(self):
        Address.find(" ", "address_id")

    @raises(NotFoundError)
    def test_finding_address_with_none_customer_id_raises_not_found_exception(self):
        Address.find(None, "address_id")

    @raises(NotFoundError)
    def test_finding_address_with_empty_address_id_raises_not_found_exception(self):
        Address.find("customer_id", " ")
