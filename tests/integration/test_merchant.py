from tests.test_helper import *
from braintree.test.nonces import Nonces

class TestMerchantGateway(unittest.TestCase):
    def setUp(self):
        self.gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret"
        )

    def test_create_merchant(self):
        gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret"
        )

        result = gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "GBR",
            "payment_methods": ["credit_card", "paypal"]
        })

        merchant = result.merchant
        self.assertIsNotNone(merchant.id)
        self.assertEqual(merchant.company_name, "name@email.com")
        self.assertEqual(merchant.email, "name@email.com")
        self.assertEqual(merchant.country_code_alpha3, "GBR")
        self.assertEqual(merchant.country_code_alpha2, "GB")
        self.assertEqual(merchant.country_code_numeric, "826")
        self.assertEqual(merchant.country_name, "United Kingdom")
        self.assertTrue(result.is_success)

        credentials = result.credentials
        self.assertIsNotNone(credentials.access_token)
        self.assertIsNotNone(credentials.expires_at)
        self.assertEqual("bearer", credentials.token_type)

    def test_returns_error_with_invalid_payment_methods(self):
        gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret"
        )

        result = gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "GBR",
            "payment_methods": ["fake_money"]
        })

        self.assertFalse(result.is_success)
        self.assertIn("One or more payment methods passed are not accepted.", result.message)

        payment_method_errors = result.errors.for_object("merchant").on("payment_methods")
        self.assertEqual(1, len(payment_method_errors))
        self.assertEqual(payment_method_errors[0].code, ErrorCodes.Merchant.PaymentMethodsAreInvalid)

    def test_create_paypal_only_merchant_that_accepts_multiple_currencies(self):
        gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret"
        )
        
        result = gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "GBR",
            "payment_methods": ["paypal"],
            "currencies": ["GBP", "USD"],
            "paypal_account": {
                "client_id": "fake_client_id",
                "client_secret": "fake_client_secret"
            }
        })

        merchant = result.merchant
        self.assertIsNotNone(merchant.id)
        self.assertEqual(merchant.company_name, "name@email.com")
        self.assertEqual(merchant.email, "name@email.com")
        self.assertEqual(merchant.country_code_alpha3, "GBR")
        self.assertEqual(merchant.country_code_alpha2, "GB")
        self.assertEqual(merchant.country_code_numeric, "826")
        self.assertEqual(merchant.country_name, "United Kingdom")
        self.assertTrue(result.is_success)

        credentials = result.credentials
        self.assertIsNotNone(credentials.access_token)
        self.assertIsNotNone(credentials.expires_at)
        self.assertEqual("bearer", credentials.token_type)

        merchant_accounts = merchant.merchant_accounts
        self.assertEqual(2, len(merchant_accounts))

        usd_merchant_account = [ma for ma in merchant_accounts if ma.id == "USD"][0]
        self.assertFalse(usd_merchant_account.default)
        self.assertEqual(usd_merchant_account.currency_iso_code, "USD")

        gbp_merchant_account = [ma for ma in merchant_accounts if ma.id == "GBP"][0]
        self.assertTrue(gbp_merchant_account.default)
        self.assertEqual(gbp_merchant_account.currency_iso_code, "GBP")

    def test_create_eu_merchant_that_accepts_multiple_currencies(self):
        gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret"
        )
        
        result = gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "GBR",
            "payment_methods": ["credit_card", "paypal"],
            "currencies": ["GBP", "USD"],
            "paypal_account": {
                "client_id": "fake_client_id",
                "client_secret": "fake_client_secret"
            }
        })

        merchant = result.merchant
        self.assertIsNotNone(merchant.id)
        self.assertEqual(merchant.email, "name@email.com")
        self.assertEqual(merchant.country_code_alpha3, "GBR")
        self.assertEqual(merchant.country_code_alpha2, "GB")
        self.assertEqual(merchant.country_code_numeric, "826")
        self.assertEqual(merchant.country_name, "United Kingdom")
        self.assertEqual(merchant.company_name, "name@email.com")
        self.assertTrue(result.is_success)

        credentials = result.credentials
        self.assertIsNotNone(credentials.access_token)
        self.assertIsNotNone(credentials.expires_at)
        self.assertEqual("bearer", credentials.token_type)

        merchant_accounts = merchant.merchant_accounts
        self.assertEqual(2, len(merchant_accounts))

        usd_merchant_account = [ma for ma in merchant_accounts if ma.id == "USD"][0]
        self.assertFalse(usd_merchant_account.default)
        self.assertEqual(usd_merchant_account.currency_iso_code, "USD")

        gbp_merchant_account = [ma for ma in merchant_accounts if ma.id == "GBP"][0]
        self.assertTrue(gbp_merchant_account.default)
        self.assertEqual(gbp_merchant_account.currency_iso_code, "GBP")

    def test_returns_error_if_invalid_currency_is_passed(self):
        result = self.gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "GBR",
            "payment_methods": ["credit_card"],
            "currencies": ["USD", "FAKE"],
            "paypal_account": {
                "client_id": "paypal_client_id",
                "client_secret": "paypal_client_secret"
            }
        })
        self.assertFalse(result.is_success)
        currencies_errors = result.errors.for_object("merchant").on("currencies")
        self.assertEqual(1, len(currencies_errors))
        self.assertEqual(ErrorCodes.Merchant.CurrenciesAreInvalid, currencies_errors[0].code)
