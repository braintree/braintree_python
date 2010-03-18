import unittest
import tests.test_helper
from braintree.credit_card import CreditCard

class TestCreditCard(unittest.TestCase):
    def test_create_raises_exception_with_bad_keys(self):
        try:
            CreditCard.create({"bad_key": "value"})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_update_raises_exception_with_bad_keys(self):
        try:
            CreditCard.update("token", {"bad_key": "value"})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_create_url(self):
        self.assertEquals(
            "http://localhost:3000/merchants/integration_merchant_id/payment_methods/all/create_via_transparent_redirect_request",
            CreditCard.create_url
        )
