from tests.test_helper import *
from braintree.sub_merchant_account.address_details import AddressDetails

class TestAddressDetails(unittest.TestCase):
    def test_repr_has_all_fields(self):
        details = AddressDetails({
            "country": "GBR",
        })

        regex = "<AddressDetails {country: 'GBR'} at \w+>"

        matches = re.match(regex, repr(details))
        self.assertTrue(matches)
