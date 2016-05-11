from tests.test_helper import *
from braintree.sub_merchant_account.address_details import AddressDetails

class TestAddressDetails(unittest.TestCase):
    def test_repr_has_all_fields(self):
        details = AddressDetails({
            "country": "GBR",
            "locality": "Liverpool",
            "postal_code": "GB 123 456",
            "region": "London",
            "street_address": "123 Main Street",
        })

        regex = "<AddressDetails {country: 'GBR', locality: 'Liverpool', postal_code: 'GB 123 456', region: 'London', street_address: '123 Main Street'} at \w+>"

        matches = re.match(regex, repr(details))
        self.assertTrue(matches)
