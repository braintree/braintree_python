from tests.test_helper import *

class TestCreditCardVerification(unittest.TestCase):
    def test_when_risk_data_is_not_included(self):
        verification = CreditCardVerification(None, {})
        self.assertEquals(verification.risk_data, None)
