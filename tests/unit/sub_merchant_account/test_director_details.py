from tests.test_helper import *
from braintree.sub_merchant_account.director_details import DirectorDetails

class TestDirectorDetails(unittest.TestCase):
    def test_repr_has_all_fields(self):
        details = DirectorDetails({
            "first_name": "Sue",
            "last_name": "Smith",
            "email": "sue@hotmail.com",
        })

        regex = "<DirectorDetails {first_name: 'Sue', last_name: 'Smith', email: 'sue@hotmail.com'} at \w+>"

        matches = re.match(regex, repr(details))
        self.assertTrue(matches)
