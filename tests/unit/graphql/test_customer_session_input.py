from tests.test_helper import unittest
from braintree.graphql import CustomerSessionInput, PhoneInput

class TestCustomerSessionInput(unittest.TestCase):
    def test_to_graphql_variables_with_all_fields(self):
        phone_input = PhoneInput.builder() \
            .country_phone_code("1") \
            .phone_number("5551234567") \
            .extension_number("1234").build()

        input_ = CustomerSessionInput.builder() \
            .email("test@example.com") \
            .phone(phone_input) \
            .device_fingerprint_id("device_fingerprint_id") \
            .paypal_app_installed(True) \
            .venmo_app_installed(False) \
            .user_agent("Mozilla") \
            .build()

        graphql_variables = input_.to_graphql_variables()

        self.assertEqual("test@example.com", graphql_variables["email"])
        self.assertEqual("device_fingerprint_id", graphql_variables["deviceFingerprintId"])
        self.assertTrue(graphql_variables["paypalAppInstalled"])
        self.assertFalse(graphql_variables["venmoAppInstalled"])
        self.assertEqual("Mozilla", graphql_variables["userAgent"])
        self.assertEqual("1", graphql_variables["phone"]["countryPhoneCode"])
        self.assertEqual("5551234567", graphql_variables["phone"]["phoneNumber"])
        self.assertEqual("1234", graphql_variables["phone"]["extensionNumber"])


    def test_to_graphql_variables_without_phone(self):
        input_ = CustomerSessionInput.builder() \
            .email("test@example.com") \
            .device_fingerprint_id("device_fingerprint_id") \
            .paypal_app_installed(True) \
            .venmo_app_installed(False).build()

        graphql_variables = input_.to_graphql_variables()

        self.assertEqual("test@example.com", graphql_variables["email"])
        self.assertEqual("device_fingerprint_id", graphql_variables["deviceFingerprintId"])
        self.assertTrue(graphql_variables["paypalAppInstalled"])
        self.assertFalse(graphql_variables["venmoAppInstalled"])
        self.assertNotIn("phone", graphql_variables)

