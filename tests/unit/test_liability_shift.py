from tests.test_helper import *
from braintree import *

class TestLiabilityShift(unittest.TestCase):
    def test_initialization_of_attributes(self):
        liability_shift = LiabilityShift(
                {
                  "responsible_party": "paypal",
                  "conditions": ["unauthorized"],
                }
        )
        self.assertEqual("paypal", liability_shift.responsible_party)
        self.assertEqual(["unauthorized"], liability_shift.conditions)
