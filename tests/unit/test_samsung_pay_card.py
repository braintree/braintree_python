from tests.test_helper import *

# NEXT_MAJOR_VERSION remove this class
# SamsungPay is deprecated
class TestSamsungPayCard(unittest.TestCase):
    def test_expiration_date(self):
        card = SamsungPayCard(None, {
            "customer_id": "12345",
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertEqual("05/2014", card.expiration_date)
    
    def test_expiration_date_no_month(self):
        card = SamsungPayCard(None, {
            "customer_id": "12345",
            "number": "4111111111111111",
            "expiration_month": "",
            "expiration_year": "2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertEqual(None, card.expiration_date)

    def test_expiration_date_no_year(self):
        card = SamsungPayCard(None, {
            "customer_id": "12345",
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertEqual(None, card.expiration_date)