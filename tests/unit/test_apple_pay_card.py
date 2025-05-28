from tests.test_helper import *

class TestApplePayCard(unittest.TestCase):
    def test_expiration_date(self):
        card = ApplePayCard(None, {
            "customer_id": "12345",
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertEqual("05/2014", card.expiration_date)
    
    def test_expiration_date_no_month(self):
        card = ApplePayCard(None, {
            "customer_id": "12345",
            "number": "4111111111111111",
            "expiration_month": "",
            "expiration_year": "2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertEqual(None, card.expiration_date)

    def test_expiration_date_no_year(self):
        card = ApplePayCard(None, {
            "customer_id": "12345",
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertEqual(None, card.expiration_date)

    def test_bin_data(self):
        card = ApplePayCard(None, {
            "business": "Unknown",
            "consumer": "Unknown",
            "corporate": "Unknown",
            "purchase": "Unknown"
        })

        self.assertEqual(CreditCard.Business.Unknown, card.business)
        self.assertEqual(CreditCard.Consumer.Unknown, card.consumer)
        self.assertEqual(CreditCard.Corporate.Unknown, card.corporate)
        self.assertEqual(CreditCard.Purchase.Unknown, card.purchase)
