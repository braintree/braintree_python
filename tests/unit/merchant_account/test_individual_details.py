from tests.test_helper import *
from braintree.merchant_account.individual_details import IndividualDetails

class TestIndividualDetails(unittest.TestCase):
    def test_repr_has_all_fields(self):
        details = IndividualDetails({
            "first_name": "Sue",
            "last_name": "Smith",
            "email": "sue@hotmail.com",
            "phone": "1112223333",
            "date_of_birth": "1980-12-05",
            "ssn_last_4": "5555",
            "address": {
                "street_address": "123 First St",
            }
        })

        regex = "<IndividualDetails {first_name: 'Sue', last_name: 'Smith', email: 'sue@hotmail.com', phone: '1112223333', date_of_birth: '1980-12-05', ssn_last_4: '5555', address_details: <AddressDetails {street_address: '123 First St'} at \w+>} at \w+>"

        matches = re.match(regex, repr(details))
        self.assertTrue(matches)
