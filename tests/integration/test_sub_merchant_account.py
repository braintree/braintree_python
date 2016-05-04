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
                    "region": "GBR",
                    "street_address": "100 Doodadew Ave",
                },
                "dba_name": "Mountain Dew Store",
                "legal_name": "PepsiCo",
                "registered_as": "sole_proprietorship",
                "registration_number": "1234",
                "tax_id": "123456789",
                "vat": "123456789",
            },
            "director": {
                "address": {
                    "locality": "Liverpool",
                    "postal_code": "12345",
                    "region": "GBR",
                    "street_address": "100 Doodadew Ave",
                },
                "date_of_birth": "1968-07-30",
                "email": "dwayne.elizondo.mountain.dew.herbert.camacho@pepsico.com",
                "first_name": "Dwayne",
                "last_name": "Camacho",
                "phone": "555-555-5555",
            },
            "funding": {
                "account_holder_name": "Dwayne Camacho",
                "account_number": "123456789",
                "currency_iso_code": "GBP",
                "descriptor": "payurdews",
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
        self.assertRegexpMatches(result.sub_merchant_account.id, "dwayneelizondomountaind")

        self.assertEquals(result.sub_merchant_account.business_details.address_details.country, "GBR")
        self.assertEquals(result.sub_merchant_account.business_details.address_details.locality, "Liverpool")
        self.assertEquals(result.sub_merchant_account.business_details.address_details.postal_code, "12345")
        self.assertEquals(result.sub_merchant_account.business_details.address_details.region, "GBR")
        self.assertEquals(result.sub_merchant_account.business_details.address_details.street_address, "100 Doodadew Ave")
        self.assertEquals(result.sub_merchant_account.business_details.dba_name, "Mountain Dew Store")
        self.assertEquals(result.sub_merchant_account.business_details.legal_name, "PepsiCo")
        self.assertEquals(result.sub_merchant_account.business_details.registered_as, "sole_proprietorship")
        self.assertEquals(result.sub_merchant_account.business_details.registration_number, "1234")
        self.assertEquals(result.sub_merchant_account.business_details.tax_id, "123456789")
        self.assertEquals(result.sub_merchant_account.business_details.vat, "123456789")

        self.assertEquals(result.sub_merchant_account.director_details.address_details.locality, "Liverpool")
        self.assertEquals(result.sub_merchant_account.director_details.address_details.postal_code, "12345")
        self.assertEquals(result.sub_merchant_account.director_details.address_details.region, "GBR")
        self.assertEquals(result.sub_merchant_account.director_details.address_details.street_address, "100 Doodadew Ave")
        self.assertEquals(result.sub_merchant_account.director_details.date_of_birth, "1968-07-30")
        self.assertEquals(result.sub_merchant_account.director_details.email, "dwayne.elizondo.mountain.dew.herbert.camacho@pepsico.com")
        self.assertEquals(result.sub_merchant_account.director_details.first_name, "Dwayne")
        self.assertEquals(result.sub_merchant_account.director_details.last_name, "Camacho")
        self.assertEquals(result.sub_merchant_account.director_details.phone, "5555555555")

        self.assertEquals(result.sub_merchant_account.funding_details.account_holder_name, 'Dwayne Camacho')
        self.assertEquals(result.sub_merchant_account.funding_details.account_number, u'\u2022\u2022\u2022\u2022\u20226789')
        self.assertEquals(result.sub_merchant_account.funding_details.currency_iso_code, "GBP")
        self.assertEquals(result.sub_merchant_account.funding_details.descriptor, "payurdews")
        self.assertEquals(result.sub_merchant_account.funding_details.routing_number, "123456789")

    def test_create_allows_an_id_to_pass(self):
        unique_token = "passed_in_token" + str(uuid1())[0:6]
        self.sub_merchant_account_create_params["id"] = unique_token

        result = SubMerchantAccount.create(self.sub_merchant_account_create_params)

        self.assertTrue(result.is_success)
        self.assertEquals(result.sub_merchant_account.id, unique_token)

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
                    "street_address": "100 Cool Ranch",
                },
                "dba_name": "Doritos Dormitory",
                "legal_name": "Frito-Lay",
                "registered_as": "sole_proprietorship",
                "registration_number": "1234",
                "tax_id": "987654321",
                "vat": "987654321",
            },
            "director": {
                "address": {
                    "locality": "London",
                    "postal_code": "54321",
                    "region": "GBR",
                    "street_address": "100 Cool Ranch",
                },
                "date_of_birth": "1968-07-30",
                "email": "geoff.keighley@G4tv.com",
                "first_name": "Geoff",
                "last_name": "Keighley",
                "phone": "555-555-6666",
            },
            "funding": {
                "account_holder_name": "Geoff Keighley",
                "account_number": "987654321",
                "currency_iso_code": "GBP",
                "descriptor": "rememberdoritos3d",
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
        self.assertEquals(result.sub_merchant_account.business_details.address_details.street_address, "100 Cool Ranch")
        self.assertEquals(result.sub_merchant_account.business_details.dba_name, "Doritos Dormitory")
        self.assertEquals(result.sub_merchant_account.business_details.legal_name, "Frito-Lay")
        self.assertEquals(result.sub_merchant_account.business_details.registered_as, "sole_proprietorship")
        self.assertEquals(result.sub_merchant_account.business_details.tax_id, "987654321")
        self.assertEquals(result.sub_merchant_account.business_details.vat, "987654321")

        self.assertEquals(result.sub_merchant_account.director_details.address_details.locality, "London")
        self.assertEquals(result.sub_merchant_account.director_details.address_details.postal_code, "54321")
        self.assertEquals(result.sub_merchant_account.director_details.address_details.region, "GBR")
        self.assertEquals(result.sub_merchant_account.director_details.address_details.street_address, "100 Cool Ranch")
        self.assertEquals(result.sub_merchant_account.director_details.date_of_birth, "1968-07-30")
        self.assertEquals(result.sub_merchant_account.director_details.email, "geoff.keighley@G4tv.com")
        self.assertEquals(result.sub_merchant_account.director_details.first_name, "Geoff")
        self.assertEquals(result.sub_merchant_account.director_details.last_name, "Keighley")
        self.assertEquals(result.sub_merchant_account.director_details.phone, "5555556666")

        self.assertEquals(result.sub_merchant_account.funding_details.account_holder_name, 'Geoff Keighley')
        self.assertEquals(result.sub_merchant_account.funding_details.account_number, u'\u2022\u2022\u2022\u2022\u20224321')
        self.assertEquals(result.sub_merchant_account.funding_details.currency_iso_code, "GBP")
        self.assertEquals(result.sub_merchant_account.funding_details.descriptor, "rememberdoritos3d")
        self.assertEquals(result.sub_merchant_account.funding_details.routing_number, "987654321")
