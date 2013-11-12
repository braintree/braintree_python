from tests.test_helper import *

class TestMerchantAccount(unittest.TestCase):
    DEPRECATED_APPLICATION_PARAMS = {
        "applicant_details": {
            "company_name": "Garbage Garage",
            "first_name": "Joe",
            "last_name": "Bloggs",
            "email": "joe@bloggs.com",
            "phone": "555-555-5555",
            "address": {
                "street_address": "123 Credibility St.",
                "postal_code": "60606",
                "locality": "Chicago",
                "region": "IL",
                },
            "date_of_birth": "10/9/1980",
            "ssn": "123-00-1234",
            "tax_id": "123456789",
            "routing_number": "122100024",
            "account_number": "43759348798"
            },
        "tos_accepted": True,
        "master_merchant_account_id": "sandbox_master_merchant_account"
    }

    VALID_APPLICATION_PARAMS = {
        "individual": {
            "first_name": "Joe",
            "last_name": "Bloggs",
            "email": "joe@bloggs.com",
            "phone": "555-555-5555",
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
            "tax_id": "123456789",
        },
        "funding": {
            "routing_number": "122100024",
            "account_number": "43759348798"
        },
        "tos_accepted": True,
        "master_merchant_account_id": "sandbox_master_merchant_account"
    }

    def test_create_accepts_deprecated_parameters(self):
        result = MerchantAccount.create(self.DEPRECATED_APPLICATION_PARAMS)

        self.assertTrue(result.is_success)
        self.assertEquals(MerchantAccount.Status.Pending, result.merchant_account.status)
        self.assertEquals("sandbox_master_merchant_account", result.merchant_account.master_merchant_account.id)

    def test_create_does_not_require_an_id(self):
        customer = Customer.create().customer
        result = MerchantAccount.create(self.VALID_APPLICATION_PARAMS)

        self.assertTrue(result.is_success)
        self.assertEquals(MerchantAccount.Status.Pending, result.merchant_account.status)
        self.assertEquals("sandbox_master_merchant_account", result.merchant_account.master_merchant_account.id)

    def test_create_allows_an_id_to_pass(self):
        params_with_id = self.VALID_APPLICATION_PARAMS.copy()
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
            {"master_merchant_account_id": "sandbox_master_merchant_account",
             "applicant_details": {},
            "tos_accepted": True}
        )
        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.MerchantAccount.ApplicantDetails.FirstNameIsRequired, result.errors.for_object("merchant_account").for_object("applicant_details").on("first_name")[0].code)

    def test_update_all_merchant_account_fields(self):
        UPDATE_PARAMS = {
            "individual": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "312-555-1234",
                "address": {
                    "street_address": "123 Fake St",
                    "postal_code": "60622",
                    "locality": "Chicago",
                    "region": "IL",
                    },
                "date_of_birth": "1970-01-01",
                "ssn": "987-65-4321",
            },
            "business": {
                "dba_name": "James's Bloggs",
                "tax_id": "987654321",
            },
            "funding": {
                "routing_number": "071000013",
                "account_number": "666666789"
            }
        }

        result = MerchantAccount.update("sandbox_sub_merchant_account", UPDATE_PARAMS)
        self.assertTrue(result.is_success)
        self.assertEquals(result.merchant_account.status, "active")
        self.assertEquals(result.merchant_account.id, "sandbox_sub_merchant_account")
        self.assertEquals(result.merchant_account.master_merchant_account.id, "sandbox_master_merchant_account")
        self.assertEquals(result.merchant_account.individual_details.first_name, "John")
        self.assertEquals(result.merchant_account.individual_details.last_name, "Doe")
        self.assertEquals(result.merchant_account.individual_details.email, "john.doe@example.com")
        self.assertEquals(result.merchant_account.individual_details.date_of_birth, "1970-01-01")
        self.assertEquals(result.merchant_account.individual_details.phone, "3125551234")
        self.assertEquals(result.merchant_account.individual_details.address_details.street_address, "123 Fake St")
        self.assertEquals(result.merchant_account.individual_details.address_details.locality, "Chicago")
        self.assertEquals(result.merchant_account.individual_details.address_details.region, "IL")
        self.assertEquals(result.merchant_account.individual_details.address_details.postal_code, "60622")
        self.assertEquals(result.merchant_account.business_details.dba_name, "James's Bloggs")

    def test_update_does_not_require_all_fields(self):
        result = MerchantAccount.update("sandbox_sub_merchant_account", { "individual": { "first_name": "Jose" } })
        self.assertTrue(result.is_success)

    def test_update_handles_unsuccessful_results(self):
        result = MerchantAccount.update("sandbox_sub_merchant_account", { "individual": { "first_name": "" } })
        self.assertFalse(result.is_success)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").on("first_name")[0].code, ErrorCodes.MerchantAccount.Individual.FirstNameIsRequired)
