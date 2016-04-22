from tests.test_helper import *

class TestSubMerchantAccount(unittest.TestCase):
    def test_create_new_sub_merchant_account_with_all_params(self):
        params = {
            "id": "sub_merchant_account",
            "status": "pending",
            "tos_accepted": "true",
            "director": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
            },
            "business": {
                "legal_name": "James's Bloggs",
                "registered_as": "sole_proprietorship",
                "address": {
                    "country": "GBR",
                }
            },
            "funding": {
                "currency_iso_code": "GBP",
            },
        }

        sub_merchant_account = SubMerchantAccount(None, params)
        self.assertEquals(sub_merchant_account.id, "sub_merchant_account")
        self.assertEquals(sub_merchant_account.status, SubMerchantAccount.Status.Pending)
        self.assertEquals(sub_merchant_account.tos_accepted, "true")
        self.assertEquals(sub_merchant_account.director_details.first_name, "John")
        self.assertEquals(sub_merchant_account.director_details.last_name, "Doe")
        self.assertEquals(sub_merchant_account.director_details.email, "john.doe@example.com")
        self.assertEquals(sub_merchant_account.business_details.legal_name, "James's Bloggs")
        self.assertEquals(sub_merchant_account.business_details.registered_as, "sole_proprietorship")
        self.assertEquals(sub_merchant_account.business_details.address_details.country, "GBR")
        self.assertEquals(sub_merchant_account.funding_details.currency_iso_code, "GBP")
