from tests.test_helper import *
from braintree.sub_merchant_account.funding_details import FundingDetails

class TestFundingDetails(unittest.TestCase):
    def test_repr_has_all_fields(self):
        details = FundingDetails({
            "currency_iso_code": "GBP",
            "account_number": "12345",
            "account_holder_name": "jim",
            "descriptor": "GBP",
            "routing_number": "GBP",
        })

        regex = "<FundingDetails {account_holder_name: 'jim', account_number: '12345', currency_iso_code: 'GBP', descriptor: 'GBP', routing_number: 'GBP'} at \w+>"

        matches = re.match(regex, repr(details))
        self.assertTrue(matches)
