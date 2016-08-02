from tests.test_helper import *
from braintree import *

class TestRiskData(unittest.TestCase):
    def test_initialization_of_attributes(self):
        risk_data = RiskData({"id": "123", "decision": "Unknown"})
        self.assertEqual("123", risk_data.id)
        self.assertEqual("Unknown", risk_data.decision)
