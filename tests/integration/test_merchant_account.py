from tests.test_helper import * 

class TestMerchantAccount(unittest.TestCase):
    VALID_APPLICATION_PARAMS = {
        "individual": {
            "first_name": "Joe",
            "last_name": "Bloggs",
            "email": "joe@bloggs.com",
            "phone": "555-123-1234",
            "address": {
                "street_address": "123 Credibility St.",
                "postal_code": "60606",
                "locality": "Chicago",
                "region": "IL",
            },
            "date_of_birth": "10/9/1980",
            "ssn": "123-00-1234",
        },
        "business": {
            "dba_name": "Garbage Garage",
            "legal_name": "Junk Jymnasium",
            "tax_id": "423456789",
            "address": {
                "street_address": "123 Reputation St.",
                "postal_code": "40222",
                "locality": "Louisville",
                "region": "KY",
            },
        },
        "funding": {
            "routing_number": "122100024",
            "account_number": "43759348798",
            "destination": MerchantAccount.FundingDestination.Bank,
            "descriptor": "Joes Bloggs KY",
        },
        "tos_accepted": True,
    }

    def test_return_all_merchant_accounts(self):
        gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret"
        )

        code = TestHelper.create_grant(gateway, {
            "merchant_public_id": "integration_merchant_id",
            "scope": "read_write"
        })

        result = gateway.oauth.create_token_from_code({
            "code": code
        })

        gateway = BraintreeGateway(
            access_token=result.credentials.access_token,
            environment=Environment.Development
        )

        result = gateway.merchant_account.all()
        merchant_accounts = [ma for ma in result.merchant_accounts.items]
        self.assertTrue(len(merchant_accounts) > 20)

    def test_returns_merchant_account_with_correct_attributes(self):
        gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret"
        )

        result = gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "GBR",
            "payment_methods": ["credit_card", "paypal"]
        })

        gateway = BraintreeGateway(
            access_token=result.credentials.access_token
        )

        result = gateway.merchant_account.all()
        merchant_accounts = [ma for ma in result.merchant_accounts.items]
        self.assertEqual(len(merchant_accounts), 1)

        merchant_account = merchant_accounts[0]
        self.assertEqual(merchant_account.currency_iso_code, "GBP")
        self.assertEqual(merchant_account.status, MerchantAccount.Status.Active)
        self.assertTrue(merchant_account.default)

    def test_find_404(self):
        with self.assertRaises(NotFoundError):
            MerchantAccount.find("not_a_real_id")

    def test_merchant_account_create_for_currency(self):
        self.gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret"
        )

        result = self.gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "GBR",
            "payment_methods": ["credit_card", "paypal"]
        })

        gateway = BraintreeGateway(
            access_token=result.credentials.access_token,
        )

        result = gateway.merchant_account.create_for_currency({
            "currency": "USD",
            "id": "custom_id"
        })

        self.assertTrue(result.is_success)
        self.assertEqual(result.merchant_account.currency_iso_code, "USD")
        self.assertEqual(result.merchant_account.id, "custom_id")

    def test_merchant_account_create_for_currency_handles_invalid_currency(self):
        self.gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret"
        )

        result = self.gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "GBR",
            "payment_methods": ["credit_card", "paypal"]
        })

        gateway = BraintreeGateway(
            access_token=result.credentials.access_token,
        )

        result = gateway.merchant_account.create_for_currency({
            "currency": "DOES_NOT_COMPUTE"
        })

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("merchant").on("currency")[0].code, ErrorCodes.Merchant.CurrencyIsInvalid)

    def test_merchant_account_create_for_currency_handles_currency_requirement(self):
        self.gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret"
        )

        result = self.gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "GBR",
            "payment_methods": ["credit_card", "paypal"]
        })

        gateway = BraintreeGateway(
            access_token=result.credentials.access_token,
        )

        result = gateway.merchant_account.create_for_currency({})

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("merchant").on("currency")[0].code, ErrorCodes.Merchant.CurrencyIsRequired)

    def test_retrieves_master_merchant_account_currency_iso_code(self):
        merchant_account = MerchantAccount.find("sandbox_master_merchant_account")
        self.assertEqual(merchant_account.currency_iso_code, "USD")
        
    def test_merchant_account_create_for_currency_merchant_account_already_existing_for_currency(self):
        self.gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret"
        )

        result = self.gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "GBR",
            "payment_methods": ["credit_card", "paypal"]
        })

        gateway = BraintreeGateway(
            access_token=result.credentials.access_token,
        )

        result = gateway.merchant_account.create_for_currency({
            "currency": "GBP",
        })

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("merchant").on("currency")[0].code, ErrorCodes.Merchant.MerchantAccountExistsForCurrency)

    def test_merchant_account_create_for_currency_merchant_account_already_existing_for_id(self):
        self.gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret"
        )

        result = self.gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "GBR",
            "payment_methods": ["credit_card", "paypal"]
        })

        gateway = BraintreeGateway(
            access_token=result.credentials.access_token,
        )

        result = gateway.merchant_account.create_for_currency({
            "currency": "GBP",
            "id": result.merchant.merchant_accounts[0].id
        })

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("merchant").on("id")[0].code, ErrorCodes.Merchant.MerchantAccountExistsForId)

