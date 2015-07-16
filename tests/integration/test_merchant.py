from tests.test_helper import *
from braintree.test.nonces import Nonces

class TestMerchantGateway(unittest.TestCase):
    def test_create_merchant(self):
        gateway = BraintreeGateway(
            client_id = "client_id$development$integration_client_id",
            client_secret = "client_secret$development$integration_client_secret",
            environment = Environment.Development
        )

        result = gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "USA",
            "payment_methods": ["credit_card", "paypal"]
        })

        merchant = result.merchant
        self.assertIsNotNone(merchant.id)
        self.assertEquals(merchant.email, "name@email.com")
        self.assertEquals(merchant.country_code_alpha3, "USA")
        self.assertEquals(merchant.country_code_alpha2, "US")
        self.assertEquals(merchant.country_code_numeric, "840")
        self.assertEquals(merchant.country_name, "United States of America")
        self.assertEquals(merchant.company_name, "name@email.com")
        self.assertTrue(result.is_success)

        credentials = result.credentials
        self.assertIsNotNone(credentials.access_token)
        self.assertIsNotNone(credentials.expires_at)
        self.assertEquals("bearer", credentials.token_type)

    def test_returns_error_with_invalid_payment_methods(self):
        gateway = BraintreeGateway(
            client_id = "client_id$development$integration_client_id",
            client_secret = "client_secret$development$integration_client_secret",
            environment = Environment.Development
        )

        result = gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "USA",
            "payment_methods": ["fake_money"]
        })

        self.assertFalse(result.is_success)
        self.assertEqual(
            result.errors.for_object("merchant").on("payment_methods")[0].code,
            ErrorCodes.Merchant.PaymentMethodsAreInvalid
        )
        self.assertIn("One or more payment methods passed are not accepted.", result.message)
