from tests.test_helper import *
from datetime import datetime
from braintree.authorization_adjustment import AuthorizationAdjustment

class TestAuthorizationAdjustment(unittest.TestCase):
    def test_constructor(self):
        attributes = {
            "amount": "-20.00",
            "timestamp": datetime(2017, 7, 12, 1, 2, 3),
            "success": True,
            "processor_response_code": "1000",
            "processor_response_text": "Approved",
        }

        authorization_adjustment = AuthorizationAdjustment(attributes)

        self.assertEqual(authorization_adjustment.amount, Decimal("-20.00"))
        self.assertEqual(authorization_adjustment.timestamp, datetime(2017, 7, 12, 1, 2, 3))
        self.assertEqual(authorization_adjustment.success, True)
        self.assertEqual(authorization_adjustment.processor_response_code, "1000")
        self.assertEqual(authorization_adjustment.processor_response_text, "Approved")

    def test_constructor_with_amount_as_None(self):
        attributes = {
            "amount": None,
            "timestamp": datetime(2017, 7, 12, 1, 2, 3),
            "success": True,
            "processor_response_code": "1000",
        }

        authorization_adjustment = AuthorizationAdjustment(attributes)

        self.assertEqual(authorization_adjustment.amount, None)
        self.assertEqual(authorization_adjustment.timestamp, datetime(2017, 7, 12, 1, 2, 3))
        self.assertEqual(authorization_adjustment.success, True)
        self.assertEqual(authorization_adjustment.processor_response_code, "1000")

    def test_constructor_without_amount(self):
        attributes = {
            "timestamp": datetime(2017, 7, 12, 1, 2, 3),
            "success": True,
            "processor_response_code": "1000",
            "processor_response_text": "Approved",
        }

        authorization_adjustment = AuthorizationAdjustment(attributes)

        self.assertEqual(authorization_adjustment.timestamp, datetime(2017, 7, 12, 1, 2, 3))
        self.assertEqual(authorization_adjustment.success, True)
        self.assertEqual(authorization_adjustment.processor_response_code, "1000")
        self.assertEqual(authorization_adjustment.processor_response_text, "Approved")
