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
        result = TestHelper.get_merchant()

        merchant_accounts = [ma for ma in result.merchant.merchant_accounts.items]
        self.assertTrue(len(merchant_accounts) > 0)

    def test_returns_merchant_account_with_correct_attributes(self):
        result = TestHelper.get_merchant()

        print(result.merchant.merchant_accounts)
        merchant_accounts = [ma for ma in result.merchant.merchant_accounts.items]
        self.assertTrue(len(merchant_accounts) > 0)

        merchant_account = merchant_accounts[0]
        self.assertEqual(merchant_account.status, MerchantAccount.Status.Active)

    def test_find_404(self):
        with self.assertRaises(NotFoundError):
            MerchantAccount.find("not_a_real_id")
    
    def test_merchant_account_create_for_currency(self):
        result = TestHelper.get_merchant()

        gateway = BraintreeGateway(
            access_token=result.credentials.access_token,
        )

        merchant_accounts = [ma for ma in result.merchant.merchant_accounts.items]
        result = gateway.merchant_account.create_for_currency({
            "currency": "JPY"
        })

        self.assertTrue(result.is_success)
        self.assertEqual(result.merchant_account.currency_iso_code, "JPY")

    def test_merchant_account_create_for_currency_handles_invalid_currency(self):
        result = TestHelper.get_merchant()

        gateway = BraintreeGateway(
            access_token=result.credentials.access_token,
        )

        result = gateway.merchant_account.create_for_currency({
            "currency": "DOES_NOT_COMPUTE"
        })

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("merchant").on("currency")[0].code, ErrorCodes.Merchant.CurrencyIsInvalid)

    def test_merchant_account_create_for_currency_handles_currency_requirement(self):
        result = TestHelper.get_merchant()

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
        result = TestHelper.get_merchant()

        gateway = BraintreeGateway(
            access_token=result.credentials.access_token,
        )

        result = gateway.merchant_account.create_for_currency({
            "currency": "EUR",
        })
        self.assertTrue(result.is_success)

        result = gateway.merchant_account.create_for_currency({
            "currency": "EUR",
        })

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("merchant").on("currency")[0].code, ErrorCodes.Merchant.MerchantAccountExistsForCurrency)
    
  
    def test_merchant_account_create_for_currency_merchant_account_already_existing_for_id(self):
        result = TestHelper.get_merchant()

        gateway = BraintreeGateway(
            access_token=result.credentials.access_token,
        )

        merchant_accounts = [ma for ma in result.merchant.merchant_accounts.items]

        result = gateway.merchant_account.create_for_currency({
            "currency": "GBP",
            "id": merchant_accounts[0].id
        })

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("merchant").on("id")[0].code, ErrorCodes.Merchant.MerchantAccountExistsForId)

