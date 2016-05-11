from tests.test_helper import *
from braintree.test.nonces import Nonces

class TestMerchantGateway(unittest.TestCase):
    def setUp(self):
        self.gateway = BraintreeGateway(
            client_id = "client_id$development$signup_client_id",
            client_secret = "client_secret$development$signup_client_secret"
        )

    def test_create_merchant(self):
        gateway = BraintreeGateway(
            client_id = "client_id$development$integration_client_id",
            client_secret = "client_secret$development$integration_client_secret"
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
            client_secret = "client_secret$development$integration_client_secret"
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

    def test_create_paypal_only_merchant_that_accepts_multiple_currencies(self):
        result = self.gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "USA",
            "payment_methods": ["paypal"],
            "currencies": ["GBP", "USD"],
            "paypal_account": {
                "client_id": "paypal_client_id",
                "client_secret": "paypal_client_secret"
            }
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

        merchant_accounts = merchant.merchant_accounts
        self.assertEquals(len(merchant_accounts), 2)

        usd_merchant_account = [ma for ma in merchant_accounts if ma.id == "USD"][0]
        self.assertTrue(usd_merchant_account.default)
        self.assertEquals(usd_merchant_account.currency_iso_code, "USD")

        gbp_merchant_account = [ma for ma in merchant_accounts if ma.id == "GBP"][0]
        self.assertFalse(gbp_merchant_account.default)
        self.assertEquals(gbp_merchant_account.currency_iso_code, "GBP")

    def test_allows_creation_of_non_US_merchant_if_onboarding_application_is_internal(self):
        result = self.gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "JPN",
            "payment_methods": ["paypal"],
            "paypal_account": {
                "client_id": "paypal_client_id",
                "client_secret": "paypal_client_secret"
            }
        })

        merchant = result.merchant
        self.assertIsNotNone(merchant.id)
        self.assertEquals(merchant.email, "name@email.com")
        self.assertEquals(merchant.country_code_alpha3, "JPN")
        self.assertEquals(merchant.country_code_alpha2, "JP")
        self.assertEquals(merchant.country_code_numeric, "392")
        self.assertEquals(merchant.country_name, "Japan")
        self.assertEquals(merchant.company_name, "name@email.com")
        self.assertTrue(result.is_success)

        credentials = result.credentials
        self.assertIsNotNone(credentials.access_token)
        self.assertIsNotNone(credentials.expires_at)
        self.assertEquals("bearer", credentials.token_type)

        merchant_accounts = merchant.merchant_accounts
        self.assertEquals(len(merchant_accounts), 1)

        usd_merchant_account = merchant_accounts[0]
        self.assertTrue(usd_merchant_account.default)
        self.assertEquals(usd_merchant_account.currency_iso_code, "JPY")

    def test_defaults_to_USD_for_non_US_merchant_if_onboarding_application_is_internal_and_country_currency_not_supported(self):
        result = self.gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "YEM",
            "payment_methods": ["paypal"],
            "paypal_account": {
                "client_id": "paypal_client_id",
                "client_secret": "paypal_client_secret"
            }
        })

        merchant = result.merchant
        self.assertIsNotNone(merchant.id)
        self.assertEquals(merchant.email, "name@email.com")
        self.assertEquals(merchant.country_code_alpha3, "YEM")
        self.assertEquals(merchant.country_code_alpha2, "YE")
        self.assertEquals(merchant.country_code_numeric, "887")
        self.assertEquals(merchant.country_name, "Yemen")
        self.assertEquals(merchant.company_name, "name@email.com")
        self.assertTrue(result.is_success)

        credentials = result.credentials
        self.assertIsNotNone(credentials.access_token)
        self.assertIsNotNone(credentials.expires_at)
        self.assertEquals("bearer", credentials.token_type)

        merchant_accounts = merchant.merchant_accounts
        self.assertEquals(len(merchant_accounts), 1)

        usd_merchant_account = merchant_accounts[0]
        self.assertTrue(usd_merchant_account.default)
        self.assertEquals(usd_merchant_account.currency_iso_code, "USD")

    def test_create_multi_currency_merchant_ignores_currencies_if_onboarding_application_not_internal(self):
        gateway = BraintreeGateway(
            client_id = "client_id$development$integration_client_id",
            client_secret = "client_secret$development$integration_client_secret"
        )

        result = gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "USA",
            "payment_methods": ["paypal"],
            "currencies": ["GBP", "USD"],
            "paypal_account": {
                "client_id": "paypal_client_id",
                "client_secret": "paypal_client_secret"
            }
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

        merchant_accounts = merchant.merchant_accounts
        self.assertEquals(len(merchant_accounts), 1)

    def test_returns_error_with_valid_payment_method_other_than_paypal_is_passed_with_multiple_currencies_provided(self):
        result = self.gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "USA",
            "payment_methods": ["credit_card", "paypal"],
            "currencies": ["GBP", "USD"],
            "paypal_account": {
                "client_id": "paypal_client_id",
                "client_secret": "paypal_client_secret"
            }
        })

        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.Merchant.PaymentMethodsAreNotAllowed, result.errors.for_object("merchant").on("payment_methods")[0].code)

    def test_returns_error_if_invalid_currency_is_passed(self):
        result = self.gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "USA",
            "payment_methods": ["credit_card", "paypal"],
            "currencies": ["GBP", "FAKE"],
            "paypal_account": {
                "client_id": "paypal_client_id",
                "client_secret": "paypal_client_secret"
            }
        })

        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.Merchant.CurrenciesAreInvalid, result.errors.for_object("merchant").on("currencies")[0].code)
