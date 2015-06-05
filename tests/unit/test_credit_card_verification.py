from tests.test_helper import *

class TestCreditCardVerification(unittest.TestCase):
    def test_when_risk_data_is_not_included(self):
        verification = CreditCardVerification(None, {})
        self.assertEquals(verification.risk_data, None)

    def test_finding_empty_id_raises_not_found_exception(self):
        try:
            CreditCardVerification.find(" ")
            self.assertTrue(False)
        except NotFoundError as e:
            self.assertTrue(True)

    def test_finding_none_raises_not_found_exception(self):
        try:
            CreditCardVerification.find(None)
            self.assertTrue(False)
        except NotFoundError as e:
            self.assertTrue(True)
