from tests.test_helper import unittest
from decimal import Decimal 
from braintree.graphql import (
    CustomerRecommendationsInput, 
    CustomerSessionInput, 
    PhoneInput, 
    MonetaryAmountInput, 
    PayPalPayeeInput, 
    PayPalPurchaseUnitInput
)

class TestCustomerRecommendationsInput(unittest.TestCase):
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

        amount = MonetaryAmountInput(currency_code="USD", value=Decimal("10.00"))
        payee = (
            PayPalPayeeInput.builder()
            .email_address("test@example.com")
            .client_id("client456")
            .build()
        ) 
        
        purchase_units = []
        purchase_unit = PayPalPurchaseUnitInput.builder(amount).payee(payee).build()
        purchase_units.append(purchase_unit)

        input_ = CustomerRecommendationsInput.builder() \
            .session_id("session_id") \
            .merchant_account_id("merchant_account_id") \
            .domain("test.com") \
            .purchase_units(purchase_units) \
            .customer(customer_input).build()

        graphql_variables = input_.to_graphql_variables()

        self.assertEqual("merchant_account_id", graphql_variables["merchantAccountId"])
        self.assertEqual("session_id", graphql_variables["sessionId"])
        self.assertEqual("test.com", graphql_variables["domain"])
        self.assertTrue(graphql_variables["purchaseUnits"])

        customer_variables = graphql_variables["customer"]
        self.assertEqual("test@example.com", customer_variables["email"])
        self.assertEqual("device_fingerprint_id", customer_variables["deviceFingerprintId"])
        self.assertTrue(customer_variables["paypalAppInstalled"])
        self.assertFalse(customer_variables["venmoAppInstalled"])
        self.assertEqual("1", customer_variables["phone"]["countryPhoneCode"])
        self.assertEqual("5551234567", customer_variables["phone"]["phoneNumber"])
        self.assertEqual("1234", customer_variables["phone"]["extensionNumber"])

        purchase_variables = graphql_variables["purchaseUnits"][0]
        self.assertEqual("10.00", purchase_variables["amount"]["value"])
        self.assertEqual("USD", purchase_variables["amount"]["currencyCode"])
        self.assertEqual("test@example.com", purchase_variables["payee"]["emailAddress"]) 

    def test_to_graphql_variables_without_optional_fields(self):
        input_ = CustomerRecommendationsInput.builder() \
            .session_id("session_id") \
            .merchant_account_id("merchant_account_id").build()

        graphql_variables = input_.to_graphql_variables()

        self.assertEqual("merchant_account_id", graphql_variables["merchantAccountId"])
        self.assertEqual("session_id", graphql_variables["sessionId"])
        self.assertNotIn("customer", graphql_variables)

