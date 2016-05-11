from tests.test_helper import *
from braintree.merchant_account.address_details import AddressDetails

class TestAddressDetails(unittest.TestCase):
    def test_repr_has_all_fields(self):
        details = AddressDetails({
            "street_address": "123 First St",
            "region": "Las Vegas",
            "locality": "NV",
            "postal_code": "89913"
        })

        regex = "<AddressDetails {street_address: '123 First St', locality: 'NV', region: 'Las Vegas', postal_code: '89913'} at \w+>"

        matches = re.match(regex, repr(details))
        self.assertTrue(matches)
