from tests.test_helper import *
from braintree import *

class TestRiskData(unittest.TestCase):
    def test_initialization_of_attributes(self):
        risk_data = RiskData({"id": "123", "decision": "Unknown"})
        self.assertEquals(risk_data.id, "123")
        self.assertEquals(risk_data.decision, "Unknown")
