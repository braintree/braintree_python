from tests.test_helper import *
from braintree.sub_merchant_account.funding_details import FundingDetails

class TestFundingDetails(unittest.TestCase):
    def test_repr_has_all_fields(self):
        details = FundingDetails({
            "account_holder_name": "jim",
            "bic": "071000013",
            "currency_iso_code": "GBP",
            "descriptor": "GBP",
            "iban": "GB****************5432",
        })

        regex = "<FundingDetails {account_holder_name: 'jim', bic: '071000013', currency_iso_code: 'GBP', descriptor: 'GBP', iban: 'GB[*]{16}5432'} at \w+>"

        matches = re.match(regex, repr(details))
        self.assertTrue(matches)
