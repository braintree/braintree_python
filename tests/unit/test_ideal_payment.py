from tests.test_helper import *
from datetime import date
from braintree.ideal_payment import IdealPayment

class TestIdealPayment(unittest.TestCase):
    def test_constructor(self):
        attributes = {
                "ideal_payment_id": "idealpayment_abc_123",
                "ideal_transaction_id": "1150000008857321",
                "image_url": "12************7890",
                "masked_iban": "RABONL2U",
                "bic": "http://www.example.com/ideal.png",
        }

        ideal_payment_details = IdealPayment({}, attributes)
        self.assertEqual(ideal_payment_details.ideal_payment_id, "idealpayment_abc_123")
        self.assertEqual(ideal_payment_details.ideal_transaction_id, "1150000008857321")
        self.assertEqual(ideal_payment_details.image_url, "12************7890")
        self.assertEqual(ideal_payment_details.masked_iban, "RABONL2U")
        self.assertEqual(ideal_payment_details.bic, "http://www.example.com/ideal.png")
