from tests.test_helper import unittest
from braintree.graphql import UpdateCustomerSessionInput, CustomerSessionInput, PhoneInput

class TestUpdateCustomerSessionInput(unittest.TestCase):
    def test_to_graphql_variables_with_all_fields(self):
        phone_input = PhoneInput.builder() \
            .country_phone_code("1") \
            .phone_number("5551234567") \
            .extension_number("1234").build()

        customer_input = CustomerSessionInput.builder() \
            .email("test@example.com") \
            .phone(phone_input) \
            .device_fingerprint_id("device_fingerprint_id") \
            .paypal_app_installed(True) \
            .venmo_app_installed(False).build()

        input_ = UpdateCustomerSessionInput.builder("session_id") \
            .merchant_account_id("merchant_account_id") \
            .customer(customer_input).build()


        graphql_variables = input_.to_graphql_variables()

        self.assertEqual("merchant_account_id", graphql_variables["merchantAccountId"])
        self.assertEqual("session_id", graphql_variables["sessionId"])

        customer_variables = graphql_variables["customer"]
        self.assertEqual("test@example.com", customer_variables["email"])
        self.assertEqual("device_fingerprint_id", customer_variables["deviceFingerprintId"])
        self.assertTrue(customer_variables["paypalAppInstalled"])
        self.assertFalse(customer_variables["venmoAppInstalled"])
        self.assertEqual("1", customer_variables["phone"]["countryPhoneCode"])
        self.assertEqual("5551234567", customer_variables["phone"]["phoneNumber"])
        self.assertEqual("1234", customer_variables["phone"]["extensionNumber"])

    def test_to_graphql_variables_without_optional_fields(self):
        input_ = UpdateCustomerSessionInput.builder("session_id") \
            .merchant_account_id("merchant_account_id").build()

        graphql_variables = input_.to_graphql_variables()

        self.assertEqual("merchant_account_id", graphql_variables["merchantAccountId"])
        self.assertEqual("session_id", graphql_variables["sessionId"])
        self.assertNotIn("customer", graphql_variables)


