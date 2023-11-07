from tests.test_helper import *
from braintree.meta_checkout_card import MetaCheckoutCard

class TestMetaCheckoutToken(unittest.TestCase):
    def test_initialization(self):
        card = MetaCheckoutCard(None, {
            "bin": "abc1234",
            "card_type": "Visa",
            "cardholder_name": "John Doe",
            "container_id": "a-container-id",
            "cryptogram": "a-cryptogram",
            "ecommerce_indicator": "01",
            "expiration_month": "05",
            "expiration_year": "2024",
            "is_network_tokenized": True,
            "last_4": "5678"
        })

        self.assertEqual(card.bin, "abc1234")
        self.assertEqual(card.card_type, "Visa")
        self.assertEqual(card.cardholder_name, "John Doe")
        self.assertEqual(card.container_id, "a-container-id")
        self.assertEqual(card.cryptogram, "a-cryptogram")
        self.assertEqual(card.ecommerce_indicator, "01")
        self.assertEqual(card.expiration_month, "05")
        self.assertEqual(card.expiration_year, "2024")
        self.assertEqual(card.is_network_tokenized, True)
        self.assertEqual(card.last_4, "5678")

    def test_expiration_date(self):
        card = MetaCheckoutCard(None, {
            "bin": "abc123",
            "card_type": "Visa",
            "cardholder_name": "John Doe",
            "container_id": "a-container-id",
            "expiration_month": "05",
            "expiration_year": "2024",
            "is_network_tokenized": True,
            "last_4": "5678"
        })

        self.assertEqual(card.expiration_date, "05/2024")

    def test_masked_number(self):
        card = MetaCheckoutCard(None, {
            "bin": "abc123",
            "card_type": "Visa",
            "cardholder_name": "John Doe",
            "container_id": "a-container-id",
            "expiration_month": "05",
            "expiration_year": "2024",
            "is_network_tokenized": True,
            "last_4": "5678"
        })

        self.assertEqual(card.masked_number, "abc123******5678")
