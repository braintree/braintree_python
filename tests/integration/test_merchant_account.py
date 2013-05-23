from random import randrange

from tests.test_helper import *

class TestMerchantAccount(unittest.TestCase):
    VALID_PARAMS = {
        "applicant_details": {
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
            "routing_number": "1234567890",
            "account_number": "43759348798"
        },
        "tos_accepted": True,
        "master_merchant_account_id": "sandbox_master_merchant_account"
    }

    def test_create(self):
        result = MerchantAccount.create(self.VALID_PARAMS)
        self.assertTrue(result.is_success)
        self.assertEquals(result.merchant_account.status, MerchantAccount.Status.Pending)
        self.assertEquals(result.merchant_account.master_merchant_account.id, "sandbox_master_merchant_account")

    def test_create_with_id(self):
        params_with_id = self.VALID_PARAMS.copy()
        rand = str(randrange(1000))
        params_with_id['id'] = 'sub_merchant_account_id' + rand
        result = MerchantAccount.create(params_with_id)
        self.assertTrue(result.is_success)
        self.assertEquals(result.merchant_account.status, MerchantAccount.Status.Pending)
        self.assertEquals(result.merchant_account.master_merchant_account.id, "sandbox_master_merchant_account")
        self.assertEquals(result.merchant_account.id, "sub_merchant_account_id" + rand)

    def test_unsuccessful_result(self):
        result = MerchantAccount.create()
        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.MerchantAccount.MasterMerchantAccountIdIsRequired, result.errors.for_object('merchant_account').on('master_merchant_account_id')[0].code)
