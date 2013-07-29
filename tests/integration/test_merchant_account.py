from tests.test_helper import *

class TestMerchantAccount(unittest.TestCase):
    VALID_PARAMS = {
            "applicant_details": {
                "company_name": "Garbage Garage",
                "first_name": "Joe",
                "last_name": "Bloggs",
                "email": "joe@bloggs.com",
                "address": {
                    "street_address": "123 Credibility St.",
                    "postal_code": "60606",
                    "locality": "Chicago",
                    "region": "IL",
                    },
                "date_of_birth": "10/9/1980",
                "ssn": "123-000-1234",
                "tax_id": "123456789",
                "routing_number": "122100024",
                "account_number": "43759348798"
                },
            "tos_accepted": True,
            "master_merchant_account_id": "sandbox_master_merchant_account"
    }

    def test_create_does_not_require_an_id(self):
        customer = Customer.create().customer
        result = MerchantAccount.create(self.VALID_PARAMS)

        self.assertTrue(result.is_success)
        self.assertEquals(MerchantAccount.Status.Pending, result.merchant_account.status)
        self.assertEquals("sandbox_master_merchant_account", result.merchant_account.master_merchant_account.id)

    def test_create_allows_an_id_to_pass(self):
        params_with_id = self.VALID_PARAMS.copy()
        rand = str(random.randrange(1000000))
        params_with_id['id'] = 'sub_merchant_account_id' + rand
        result = MerchantAccount.create(params_with_id)

        self.assertTrue(result.is_success)
        self.assertEquals(MerchantAccount.Status.Pending, result.merchant_account.status)
        self.assertEquals(params_with_id['id'], result.merchant_account.id)
        self.assertEquals("sandbox_master_merchant_account", result.merchant_account.master_merchant_account.id)

    def test_create_handles_unsuccessful_results(self):
        result = MerchantAccount.create({})
        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.MerchantAccount.MasterMerchantAccountIdIsRequired, result.errors.for_object("merchant_account").on("master_merchant_account_id")[0].code)
        
    def test_create_requires_all_fields(self):
        result = MerchantAccount.create(
            {"master_merchant_account_id": "sandbox_master_merchant_account"}
        )
        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.MerchantAccount.ApplicantDetails.FirstNameIsRequired, result.errors.for_object("merchant_account").for_object("applicant_details").on("first_name")[0].code) 
