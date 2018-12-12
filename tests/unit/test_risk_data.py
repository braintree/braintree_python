from tests.test_helper import *
from braintree import *

class TestRiskData(unittest.TestCase):
    def test_initialization_of_attributes(self):
        risk_data = RiskData({"id": "123", "decision": "Unknown", "device_data_captured": True, "fraud_service_provider": "some_fraud_provider"})
        self.assertEqual("123", risk_data.id)
        self.assertEqual("Unknown", risk_data.decision)
        self.assertEqual(True, risk_data.device_data_captured)
        self.assertEqual("some_fraud_provider", risk_data.fraud_service_provider)
