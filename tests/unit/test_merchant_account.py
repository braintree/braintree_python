from tests.test_helper import *

class TestMerchantAccount(unittest.TestCase):
    def test_create_new_merchant_account_with_all_params(self):
        params = {
            "id": "sub_merchant_account",
            "status": "active",
            "master_merchant_account": {
                "id": "master_merchant_account",
                "status": "active"
            },
            "individual": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "date_of_birth": "1970-01-01",
                "phone": "3125551234",
                "ssn_last_4": "6789",
                "address": {
                    "street_address": "123 Fake St",
                    "locality": "Chicago",
                    "region": "IL",
                    "postal_code": "60622",
                }
            },
            "business": {
                "dba_name": "James's Bloggs",
                "tax_id": "123456789",
            },
            "funding": {
                "account_number_last_4": "8798",
                "routing_number": "071000013",
                "descriptor": "Joes Bloggs MI",
            }
        }

        merchant_account = MerchantAccount(None, params)

        self.assertEqual(merchant_account.status, "active")
        self.assertEqual(merchant_account.id, "sub_merchant_account")
        self.assertEqual(merchant_account.master_merchant_account.id, "master_merchant_account")
        self.assertEqual(merchant_account.master_merchant_account.status, "active")
        self.assertEqual(merchant_account.individual_details.first_name, "John")
        self.assertEqual(merchant_account.individual_details.last_name, "Doe")
        self.assertEqual(merchant_account.individual_details.email, "john.doe@example.com")
        self.assertEqual(merchant_account.individual_details.date_of_birth, "1970-01-01")
        self.assertEqual(merchant_account.individual_details.phone, "3125551234")
        self.assertEqual(merchant_account.individual_details.ssn_last_4, "6789")
        self.assertEqual(merchant_account.individual_details.address_details.street_address, "123 Fake St")
        self.assertEqual(merchant_account.individual_details.address_details.locality, "Chicago")
        self.assertEqual(merchant_account.individual_details.address_details.region, "IL")
        self.assertEqual(merchant_account.individual_details.address_details.postal_code, "60622")
        self.assertEqual(merchant_account.business_details.dba_name, "James's Bloggs")
        self.assertEqual(merchant_account.business_details.tax_id, "123456789")
        self.assertEqual(merchant_account.funding_details.account_number_last_4, "8798")
        self.assertEqual(merchant_account.funding_details.routing_number, "071000013")
        self.assertEqual(merchant_account.funding_details.descriptor, "Joes Bloggs MI")
