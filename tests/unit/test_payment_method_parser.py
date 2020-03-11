from tests.test_helper import *
from braintree.payment_method_parser import parse_payment_method
from unittest.mock import MagicMock

class TestPaymentMethodParser(unittest.TestCase):
    def test_parse_response_returns_a_credit_card(self):
        credit_card = parse_payment_method(BraintreeGateway(None), {
            "credit_card": {"bin": "411111", "last_4": "1111"}
        })

        self.assertEqual(CreditCard, credit_card.__class__)
        self.assertEqual("411111", credit_card.bin)
        self.assertEqual("1111", credit_card.last_4)

    def test_parse_response_returns_a_paypal_account(self):
        paypal_account = parse_payment_method(BraintreeGateway(None), {
            "paypal_account": {"token": "1234", "default": False}
        })

        self.assertEqual(PayPalAccount, paypal_account.__class__)
        self.assertEqual("1234", paypal_account.token)
        self.assertFalse(paypal_account.default)

    def test_parse_response_returns_an_unknown_payment_method(self):
        unknown_payment_method = parse_payment_method(BraintreeGateway(None), {
            "new_fancy_payment_method": {
                "token": "1234",
                "default": True,
                "other_fancy_thing": "is-shiny"
            }
        })

        self.assertEqual(UnknownPaymentMethod, unknown_payment_method.__class__)
        self.assertEqual("1234", unknown_payment_method.token)
        self.assertTrue(unknown_payment_method.default)

