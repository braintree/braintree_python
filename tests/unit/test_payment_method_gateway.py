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

    def test_create_signature(self):
        actual_signature = PaymentMethod.signature("create")

        expected_signature = [
            "billing_address_id",
            "cardholder_name",
            "customer_id",
            "cvv",
            "device_data",
            "device_session_id",
            "expiration_date",
            "expiration_month",
            "expiration_year",
            "number",
            "payment_method_nonce",
            "token",
            {
                "billing_address": Address.create_signature()},
            {
                "options": [
                    "fail_on_duplicate_payment_method",
                    "make_default",
                    "verification_merchant_account_id",
                    "verify_card",
                ]
            }
        ]

        self.assertEqual(expected_signature, actual_signature)

    def test_update_signature(self):
        actual_signature = PaymentMethod.update_signature()

        expected_signature = [
            "billing_address_id",
            "cardholder_name",
            "cvv",
            "device_session_id",
            "expiration_date",
            "expiration_month",
            "expiration_year",
            "number",
            "token",
            "venmo_sdk_payment_method_code",
            "device_data",
            "fraud_merchant_id",
            "payment_method_nonce",
            {
                "options": [
                    "make_default",
                    "verify_card",
                    "verification_merchant_account_id",
                    "venmo_sdk_session"
                ]
            },
            {
                "billing_address" : Address.update_signature() + [{"options": ["update_existing"]}]
            }
        ]

        self.assertEqual(expected_signature, actual_signature)

    def test_nonce_grant_params(self):
        """
        We validate parameters to PaymentMethod.grant properly
        """
        payment_method_gateway = PaymentMethodGateway(BraintreeGateway(None))
        with self.assertRaises(ValueError):
            payment_method_gateway.grant("", False)

        with self.assertRaises(ValueError):
            payment_method_gateway.grant("\t", False)

        with self.assertRaises(ValueError):
            payment_method_gateway.grant(None, False)

    def test_nonce_revoke_params(self):
        payment_method_gateway = PaymentMethodGateway(BraintreeGateway(None))
        with self.assertRaises(ValueError):
            payment_method_gateway.revoke("")

        with self.assertRaises(ValueError):
            payment_method_gateway.revoke("\t")

        with self.assertRaises(ValueError):
            payment_method_gateway.revoke(None)
