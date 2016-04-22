from tests.test_helper import *
from braintree.sub_merchant_account.business_details import BusinessDetails

class TestBusinessDetails(unittest.TestCase):
    def test_repr_has_all_fields(self):
        details = BusinessDetails({
            "legal_name": "Suenami Restaurant Group",
            "registered_as": "sole_proprietorship",
            "address": {
                "country": "GBR",
            }
        })

        regex = "<BusinessDetails {legal_name: 'Suenami Restaurant Group', registered_as: 'sole_proprietorship', address_details: <AddressDetails {country: 'GBR'} at \w+>} at \w+>"

        matches = re.match(regex, repr(details))
        self.assertTrue(matches)
