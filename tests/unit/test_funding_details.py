from tests.test_helper import *

class TestFundingDetails(unittest.TestCase):
    def test_repr_has_all_fields(self):
        details = FundingDetails({
            "destination": "bank",
            "routing_number": "11112222",
            "account_number_last_4": "3333",
            "email": "lucyloo@work.com",
            "mobile_phone": "9998887777"
        })

        regex = "<FundingDetails {account_number_last_4: '3333', routing_number: '11112222', destination: 'bank', email: 'lucyloo@work.com', mobile_phone: '9998887777'} at \w+>"

        matches = re.match(regex, repr(details))
        self.assertTrue(matches)
