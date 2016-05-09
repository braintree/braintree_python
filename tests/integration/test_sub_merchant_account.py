from tests.test_helper import *
from uuid import uuid1

class TestSubMerchantAccount(unittest.TestCase):
    def setUp(self):
        self.old_merchant_id = Configuration.merchant_id
        self.old_public_key = Configuration.public_key
        self.old_private_key = Configuration.private_key

        Configuration.merchant_id = "v2_marketplace_merchant"
        Configuration.public_key = "v2_marketplace_merchant_public_key"
        Configuration.private_key = "v2_marketplace_merchant_private_key"

        self.sub_merchant_account_create_params = {
            "business": {
                "address": {
                    "country": "GBR",
                    "locality": "Liverpool",
                    "postal_code": "12345",
                    "region": "JS",
                    "street_address": "100 Main Ave",
                },
                "dba_name": "Generic Retail Shop",
                "legal_name": "Generic's Store",
                "registered_as": "sole_proprietorship",
                "registration_number": "1234",
                "tax_id": "123456789",
                "vat": "123456789",
            },
            "director": {
                "address": {
                    "country": "GBR",
                    "locality": "Liverpool",
                    "postal_code": "12345",
                    "region": "JS",
                    "street_address": "100 Main Ave",
                },
                "date_of_birth": "1968-07-30",
                "email": "johndoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "5555555555",
            },
            "funding": {
                "account_holder_name": "John Doe",
                "account_number": "123456789",
                "currency_iso_code": "GBP",
                "descriptor": "genericdescriptor",
                "routing_number": "123456789",
            },
            "tos_accepted": True,
        }

    def tearDown(self):
        Configuration.merchant_id = self.old_merchant_id
        Configuration.public_key = self.old_public_key
        Configuration.private_key = self.old_private_key

    def test_create_sub_merchant_account_with_valid_params_and_no_id(self):
        result = SubMerchantAccount.create(self.sub_merchant_account_create_params)

        self.assertTrue(result.is_success)
        self.assertEquals(SubMerchantAccount.Status.Pending, result.sub_merchant_account.status)
        self.assertRegexpMatches(result.sub_merchant_account.id, "johndoeexamplecom")

        self.assertEquals(result.sub_merchant_account.business_details.address_details.country, "GBR")
        self.assertEquals(result.sub_merchant_account.business_details.address_details.locality, "Liverpool")
        self.assertEquals(result.sub_merchant_account.business_details.address_details.postal_code, "12345")
        self.assertEquals(result.sub_merchant_account.business_details.address_details.region, "JS")
        self.assertEquals(result.sub_merchant_account.business_details.address_details.street_address, "100 Main Ave")
        self.assertEquals(result.sub_merchant_account.business_details.dba_name, "Generic Retail Shop")
        self.assertEquals(result.sub_merchant_account.business_details.legal_name, "Generic's Store")
        self.assertEquals(result.sub_merchant_account.business_details.registered_as, "sole_proprietorship")
        self.assertEquals(result.sub_merchant_account.business_details.registration_number, "1234")
        self.assertEquals(result.sub_merchant_account.business_details.tax_id, "123456789")
        self.assertEquals(result.sub_merchant_account.business_details.vat, "123456789")

        self.assertEquals(result.sub_merchant_account.director_details.address_details.country, "GBR")
        self.assertEquals(result.sub_merchant_account.director_details.address_details.locality, "Liverpool")
        self.assertEquals(result.sub_merchant_account.director_details.address_details.postal_code, "12345")
        self.assertEquals(result.sub_merchant_account.director_details.address_details.region, "JS")
        self.assertEquals(result.sub_merchant_account.director_details.address_details.street_address, "100 Main Ave")
        self.assertEquals(result.sub_merchant_account.director_details.date_of_birth, "1968-07-30")
        self.assertEquals(result.sub_merchant_account.director_details.email, "johndoe@example.com")
        self.assertEquals(result.sub_merchant_account.director_details.first_name, "John")
        self.assertEquals(result.sub_merchant_account.director_details.last_name, "Doe")
        self.assertEquals(result.sub_merchant_account.director_details.phone, "5555555555")

        self.assertEquals(result.sub_merchant_account.funding_details.account_holder_name, "John Doe")
        self.assertEquals(result.sub_merchant_account.funding_details.account_number, u"\u2022\u2022\u2022\u2022\u20226789")
        self.assertEquals(result.sub_merchant_account.funding_details.currency_iso_code, "GBP")
        self.assertEquals(result.sub_merchant_account.funding_details.descriptor, "genericdescriptor")
        self.assertEquals(result.sub_merchant_account.funding_details.routing_number, "123456789")

    def test_create_allows_an_id_to_pass(self):
        unique_token = "passed_in_token" + str(uuid1())[0:6]
        self.sub_merchant_account_create_params["id"] = unique_token

        result = SubMerchantAccount.create(self.sub_merchant_account_create_params)

        self.assertTrue(result.is_success)
        self.assertEquals(result.sub_merchant_account.id, unique_token)

<<<<<<< HEAD
    def test_create_includes_fields_required_for_verification(self):
        del(self.sub_merchant_account_create_params["business"]["dba_name"])

        result = SubMerchantAccount.create(self.sub_merchant_account_create_params)

        self.assertTrue(result.is_success)
        self.assertTrue("business.dba_name" in result.sub_merchant_account.fields_required_for_verification)
=======
    def test_create_with_missing_fields(self):
        self.sub_merchant_account_create_params["director"].pop("first_name")
        result = SubMerchantAccount.create(self.sub_merchant_account_create_params)

        self.assertFalse(result.is_success)

        self.assertEquals(1, result.errors.size)
        self.assertEquals(ErrorCodes.SubMerchantAccount.Director.FirstNameIsRequired, result.errors.for_object("sub_merchant_account").on("first_name")[0].code)


    def test_create_with_invalid_options(self):
        self.sub_merchant_account_create_params["director"]["date_of_birth"] = "1776-01-01"
        result = SubMerchantAccount.create(self.sub_merchant_account_create_params)

        self.assertFalse(result.is_success)

        self.assertEquals(1, result.errors.size)
        self.assertEquals(ErrorCodes.SubMerchantAccount.Director.BirthDateMustBe100YearsOldOrYounger, result.errors.for_object("sub_merchant_account").on("birth_date")[0].code)
>>>>>>> BTMKPL-264 - Handle validation errors for sub merchant account create/update

    def test_update_with_valid_options(self):
        sub_merchant_account = SubMerchantAccount.create(self.sub_merchant_account_create_params).sub_merchant_account
        director_id = sub_merchant_account.director_details.id

        result = SubMerchantAccount.update(sub_merchant_account.id, {
            "business": {
                "address": {
                    "country": "GBR",
                    "locality": "London",
                    "postal_code": "54321",
                    "region": "GBR",
                    "street_address": "123 Main Street",
                },
                "dba_name": "Non-Generic Retail Shop",
                "legal_name": "Non-Generic Store",
                "registered_as": "sole_proprietorship",
                "registration_number": "4321",
                "tax_id": "987654321",
                "vat": "987654321",
            },
            "director": {
                "address": {
                    "locality": "London",
                    "postal_code": "54321",
                    "region": "GBR",
                    "street_address": "123 Main Street",
                },
                "date_of_birth": "1968-07-30",
                "email": "janedot@example.com",
                "first_name": "Jane",
                "id": director_id,
                "last_name": "Dot",
                "phone": "5555556666",
            },
            "funding": {
                "account_holder_name": "Jane Dot",
                "account_number": "987654321",
                "currency_iso_code": "GBP",
                "descriptor": "nongenericdescriptor",
                "routing_number": "987654321",
            },
            "tos_accepted": True,
        })

        self.assertTrue(result.is_success)
        sub_merchant_account = result.sub_merchant_account

        self.assertEquals(result.sub_merchant_account.business_details.address_details.country, "GBR")
        self.assertEquals(result.sub_merchant_account.business_details.address_details.locality, "London")
        self.assertEquals(result.sub_merchant_account.business_details.address_details.postal_code, "54321")
        self.assertEquals(result.sub_merchant_account.business_details.address_details.region, "GBR")
        self.assertEquals(result.sub_merchant_account.business_details.address_details.street_address, "123 Main Street")
        self.assertEquals(result.sub_merchant_account.business_details.dba_name, "Non-Generic Retail Shop")
        self.assertEquals(result.sub_merchant_account.business_details.legal_name, "Non-Generic Store")
        self.assertEquals(result.sub_merchant_account.business_details.registered_as, "sole_proprietorship")
        self.assertEquals(result.sub_merchant_account.business_details.tax_id, "987654321")
        self.assertEquals(result.sub_merchant_account.business_details.vat, "987654321")

        self.assertEquals(result.sub_merchant_account.director_details.address_details.locality, "London")
        self.assertEquals(result.sub_merchant_account.director_details.address_details.postal_code, "54321")
        self.assertEquals(result.sub_merchant_account.director_details.address_details.region, "GBR")
        self.assertEquals(result.sub_merchant_account.director_details.address_details.street_address, "123 Main Street")
        self.assertEquals(result.sub_merchant_account.director_details.date_of_birth, "1968-07-30")
        self.assertEquals(result.sub_merchant_account.director_details.email, "janedot@example.com")
        self.assertEquals(result.sub_merchant_account.director_details.first_name, "Jane")
        self.assertEquals(result.sub_merchant_account.director_details.last_name, "Dot")
        self.assertEquals(result.sub_merchant_account.director_details.phone, "5555556666")

        self.assertEquals(result.sub_merchant_account.funding_details.account_holder_name, "Jane Dot")
        self.assertEquals(result.sub_merchant_account.funding_details.account_number, u"\u2022\u2022\u2022\u2022\u20224321")
        self.assertEquals(result.sub_merchant_account.funding_details.currency_iso_code, "GBP")
        self.assertEquals(result.sub_merchant_account.funding_details.descriptor, "nongenericdescriptor")
        self.assertEquals(result.sub_merchant_account.funding_details.routing_number, "987654321")

    def test_update_with_invalid_options(self):
        sub_merchant_account = SubMerchantAccount.create(self.sub_merchant_account_create_params).sub_merchant_account
        director_id = sub_merchant_account.director_details.id

        result = SubMerchantAccount.update(sub_merchant_account.id, {
            "director": {
                "date_of_birth": "1776-07-30",
                "id": director_id,
            },
        })

        self.assertFalse(result.is_success)

        self.assertEquals(1, result.errors.size)
        self.assertEquals(ErrorCodes.SubMerchantAccount.Director.BirthDateMustBe100YearsOldOrYounger, result.errors.for_object("sub_merchant_account").on("birth_date")[0].code)
