from tests.test_helper import *

class TestAndroidPayCard(unittest.TestCase):
    def test_expiration_date(self):
        card = AndroidPayCard(None, {
            "customer_id": "12345",
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertEqual("05/2014", card.expiration_date)
    
    def test_expiration_date_no_month(self):
        card = AndroidPayCard(None, {
            "customer_id": "12345",
            "number": "4111111111111111",
            "expiration_month": "",
            "expiration_year": "2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertEqual(None, card.expiration_date)

    def test_expiration_date_no_year(self):
        card = AndroidPayCard(None, {
            "customer_id": "12345",
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertEqual(None, card.expiration_date)

    def test_bin_data(self):
        card = AndroidPayCard(None, {
            "customer_id": "12345",
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "2014",
            "cvv": "100",
            "cardholder_name": "John Doe",
            "business": "Yes",
            "consumer": "No",
            "corporate": "Yes",
            "purchase": "No",
        })

        self.assertEqual(CreditCard.Business.Yes, card.business)
        self.assertEqual(CreditCard.Consumer.No, card.consumer)
        self.assertEqual(CreditCard.Corporate.Yes, card.corporate)
        self.assertEqual(CreditCard.Purchase.No, card.purchase)

