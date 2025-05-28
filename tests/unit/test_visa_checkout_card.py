from tests.test_helper import *
from braintree.visa_checkout_card import VisaCheckoutCard

class TestVisaCheckoutCard(unittest.TestCase):
    def test_expiration_date(self):
        card = VisaCheckoutCard(None, {
            "customer_id": "12345",
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertEqual("05/2014", card.expiration_date)
    
    def test_expiration_date_no_month(self):
        card = VisaCheckoutCard(None, {
            "customer_id": "12345",
            "number": "4111111111111111",
            "expiration_month": "",
            "expiration_year": "2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertEqual(None, card.expiration_date)

    def test_expiration_date_no_year(self):
        card = VisaCheckoutCard(None, {
            "customer_id": "12345",
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertEqual(None, card.expiration_date)

    def test_bin_data(self):
        card = VisaCheckoutCard(None, {
            "business": "No",
            "consumer": "Yes",
            "corporate": "No",
            "purchase": "Yes",
        })

        self.assertEqual(card.business, CreditCard.Business.No)
        self.assertEqual(card.consumer, CreditCard.Consumer.Yes)
        self.assertEqual(card.corporate, CreditCard.Corporate.No)
        self.assertEqual(card.purchase, CreditCard.Purchase.Yes)
