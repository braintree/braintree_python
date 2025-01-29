from tests.test_helper import unittest
from braintree.graphql import PhoneInput

class TestPhoneInput(unittest.TestCase):
    def test_to_graphql_variables(self):
        input_ = PhoneInput.builder() \
            .country_phone_code("1") \
            .phone_number("5551234567") \
            .extension_number("1234").build();

        graphql_variables = input_.to_graphql_variables()

        self.assertEqual("1",graphql_variables["countryPhoneCode"])
        self.assertEqual("5551234567",graphql_variables["phoneNumber"])
        self.assertEqual("1234",graphql_variables["extensionNumber"])
