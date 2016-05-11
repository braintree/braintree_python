from tests.test_helper import *
from braintree.sub_merchant_account.business_details import BusinessDetails

class TestBusinessDetails(unittest.TestCase):
    def test_repr_has_all_fields(self):
        details = BusinessDetails({
            "address": {
                "country": "GBR",
                "locality": "Liverpool",
                "postal_code": "GB 123 456",
                "region": "London",
                "street_address": "123 Main Street",
            },
            "dba_name": "Suenami Co",
            "legal_name": "Suenami Restaurant Group",
            "registered_as": "sole_proprietorship",
            "registration_number": "123",
            "tax_id": "456",
            "vat": "789",
        })

        regex = "<BusinessDetails {address_details: <AddressDetails {country: 'GBR', locality: 'Liverpool', postal_code: 'GB 123 456', region: 'London', street_address: '123 Main Street'} at \w+>, dba_name: 'Suenami Co', legal_name: 'Suenami Restaurant Group', registered_as: 'sole_proprietorship', registration_number: '123', tax_id: '456', vat: '789'} at \w+"

        matches = re.match(regex, repr(details))
        self.assertTrue(matches)
