from tests.test_helper import *
from braintree.payment_method_gateway import PaymentMethodGateway

class TestPaymentMethodGateway(unittest.TestCase):
    def test_parse_response_returns_a_credit_card(self):
        payment_method_gateway = PaymentMethodGateway(BraintreeGateway(None))
        credit_card = payment_method_gateway._parse_payment_method({
            "credit_card": {"bin": "411111", "last_4": "1111"}
        })

        self.assertEquals(credit_card.__class__, CreditCard)
        self.assertEquals(credit_card.bin, "411111")
        self.assertEquals(credit_card.last_4, "1111")

    def test_parse_response_returns_a_paypal_account(self):
        payment_method_gateway = PaymentMethodGateway(BraintreeGateway(None))
        paypal_account = payment_method_gateway._parse_payment_method({
            "paypal_account": {"token": "1234", "default": False}
        })

        self.assertEquals(paypal_account.__class__, PayPalAccount)
        self.assertEquals(paypal_account.token, "1234")
        self.assertFalse(paypal_account.default)

    def test_parse_response_returns_an_unknown_payment_method(self):
        payment_method_gateway = PaymentMethodGateway(BraintreeGateway(None))
        unknown_payment_method = payment_method_gateway._parse_payment_method({
            "new_fancy_payment_method": {
                "token": "1234",
                "default": True,
                "other_fancy_thing": "is-shiny"
            }
        })

        self.assertEquals(unknown_payment_method.__class__, UnknownPaymentMethod)
        self.assertEquals(unknown_payment_method.token, "1234")
        self.assertTrue(unknown_payment_method.default)
