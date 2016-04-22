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
            "tos_accepted": True,
            "director": {
                "first_name": "Joe",
                "last_name": "Bloggs",
                "email": "joe@bloggs.com",
            },
            "business": {
                "legal_name": "Junk Jymnasium",
                "registered_as": "sole_proprietorship",
                "address": {
                    "country": "GBR",
                },
            },
            "funding": {
                "currency_iso_code": "GBP",
            },
        }

    def tearDown(self):
        Configuration.merchant_id = self.old_merchant_id
        Configuration.public_key = self.old_public_key
        Configuration.private_key = self.old_private_key

    def test_create_sub_merchant_account_with_valid_params_and_no_id(self):
        result = SubMerchantAccount.create(self.sub_merchant_account_create_params)

        self.assertTrue(result.is_success)
        self.assertEquals(SubMerchantAccount.Status.Pending, result.sub_merchant_account.status)
        self.assertRegexpMatches(result.sub_merchant_account.id, "joebloggscom")
        self.assertEquals(result.sub_merchant_account.director_details.first_name, "Joe")
        self.assertEquals(result.sub_merchant_account.director_details.last_name, "Bloggs")
        self.assertEquals(result.sub_merchant_account.director_details.email, "joe@bloggs.com")
        self.assertEquals(result.sub_merchant_account.business_details.legal_name, "Junk Jymnasium")
        self.assertEquals(result.sub_merchant_account.business_details.registered_as, "sole_proprietorship")
        self.assertEquals(result.sub_merchant_account.business_details.address_details.country, "GBR")
        self.assertEquals(result.sub_merchant_account.funding_details.currency_iso_code, "GBP")

    def test_create_allows_an_id_to_pass(self):
        unique_token = "passed_in_token" + str(uuid1())[0:6]
        self.sub_merchant_account_create_params["id"] = unique_token

        result = SubMerchantAccount.create(self.sub_merchant_account_create_params)

        self.assertTrue(result.is_success)
        self.assertEquals(result.sub_merchant_account.id, unique_token)
