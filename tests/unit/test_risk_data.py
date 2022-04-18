from tests.test_helper import *
from braintree import *

class TestRiskData(unittest.TestCase):
    def test_initialization_of_attributes(self):
        risk_data = RiskData(
                {
                    "id": "123",
                    "decision": "Unknown",
                    "device_data_captured": True,
                    "fraud_service_provider":
                    "some_fraud_provider",
                    "transaction_risk_score": "42",
                    "decision_reasons": ["reason"],
                    "liability_shift": {
                          "responsible_party": "paypal",
                          "conditions": ["unauthorized"],
                        }
                    }
                )
        self.assertEqual("123", risk_data.id)
        self.assertEqual("Unknown", risk_data.decision)
        self.assertEqual(True, risk_data.device_data_captured)
        self.assertEqual("some_fraud_provider", risk_data.fraud_service_provider)
        self.assertEqual("42", risk_data.transaction_risk_score)
        self.assertEqual(["reason"], risk_data.decision_reasons)
        self.assertEqual("paypal", risk_data.liability_shift.responsible_party)
        self.assertEqual(["unauthorized"], risk_data.liability_shift.conditions)
