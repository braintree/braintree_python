from tests.test_helper import *
from braintree.sub_merchant_account.funding_details import FundingDetails

class TestFundingDetails(unittest.TestCase):
    def test_repr_has_all_fields(self):
        details = FundingDetails({
            "currency_iso_code": "GBP"
        })

        regex = "<FundingDetails {currency_iso_code: 'GBP'} at \w+>"

        matches = re.match(regex, repr(details))
        self.assertTrue(matches)
