from tests.test_helper import *

class TestSubMerchantAccount(unittest.TestCase):
    def test_create_new_sub_merchant_account_with_all_params(self):
        params = {
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
            "contacts": [{
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
            }],
            "funding": {
                "account_holder_name": "John Doe",
                "bic": "071000013",
                "currency_iso_code": "GBP",
                "descriptor": "genericdescriptor",
                "iban": "GB****************5432",
            },
            "tos_accepted": True,
            "status": "pending",
            "id": "sub_merchant_account",
            "fields_required_for_verification": [
                "contact.address.street_address",
                "business.website",
            ],
        }

        sub_merchant_account = SubMerchantAccount(None, params)
        self.assertEquals(sub_merchant_account.id, "sub_merchant_account")
        self.assertEquals(sub_merchant_account.status, SubMerchantAccount.Status.Pending)
        self.assertEquals(sub_merchant_account.tos_accepted, True)
        self.assertEquals(sub_merchant_account.contacts[0].first_name, "John")
        self.assertEquals(sub_merchant_account.contacts[0].last_name, "Doe")
        self.assertEquals(sub_merchant_account.contacts[0].email, "johndoe@example.com")
        self.assertEquals(sub_merchant_account.contacts[0].phone, "5555555555")
        self.assertEquals(sub_merchant_account.contacts[0].date_of_birth, "1968-07-30")
        self.assertEquals(sub_merchant_account.contacts[0].address_details.country, "GBR")
        self.assertEquals(sub_merchant_account.contacts[0].address_details.locality, "Liverpool")
        self.assertEquals(sub_merchant_account.contacts[0].address_details.postal_code, "12345")
        self.assertEquals(sub_merchant_account.contacts[0].address_details.region, "JS")
        self.assertEquals(sub_merchant_account.contacts[0].address_details.street_address, "100 Main Ave")
        self.assertEquals(sub_merchant_account.business_details.legal_name, "Generic's Store")
        self.assertEquals(sub_merchant_account.business_details.dba_name, "Generic Retail Shop")
        self.assertEquals(sub_merchant_account.business_details.registered_as, "sole_proprietorship")
        self.assertEquals(sub_merchant_account.business_details.registration_number, "1234")
        self.assertEquals(sub_merchant_account.business_details.tax_id, "123456789")
        self.assertEquals(sub_merchant_account.business_details.vat, "123456789")
        self.assertEquals(sub_merchant_account.business_details.address_details.country, "GBR")
        self.assertEquals(sub_merchant_account.business_details.address_details.locality, "Liverpool")
        self.assertEquals(sub_merchant_account.business_details.address_details.postal_code, "12345")
        self.assertEquals(sub_merchant_account.business_details.address_details.region, "JS")
        self.assertEquals(sub_merchant_account.business_details.address_details.street_address, "100 Main Ave")
        self.assertEquals(sub_merchant_account.funding_details.account_holder_name, "John Doe")
        self.assertEquals(sub_merchant_account.funding_details.currency_iso_code, "GBP")
        self.assertEquals(sub_merchant_account.funding_details.descriptor, "genericdescriptor")
        self.assertEquals(sub_merchant_account.funding_details.bic, "071000013")
        self.assertEquals(sub_merchant_account.funding_details.iban, "GB****************5432")
        self.assertEquals(sub_merchant_account.fields_required_for_verification, ["contact.address.street_address", "business.website"])
