from tests.test_helper import *
from braintree.payment_method_gateway import PaymentMethodGateway
if sys.version_info[0] == 2:
    from mock import MagicMock
else:
    from unittest.mock import MagicMock

class TestPaymentMethodGateway(unittest.TestCase):
    def test_parse_response_returns_a_credit_card(self):
        payment_method_gateway = PaymentMethodGateway(BraintreeGateway(None))
        credit_card = payment_method_gateway._parse_payment_method({
            "credit_card": {"bin": "411111", "last_4": "1111"}
        })

        self.assertEqual(CreditCard, credit_card.__class__)
        self.assertEqual("411111", credit_card.bin)
        self.assertEqual("1111", credit_card.last_4)

    def test_parse_response_returns_a_paypal_account(self):
        payment_method_gateway = PaymentMethodGateway(BraintreeGateway(None))
        paypal_account = payment_method_gateway._parse_payment_method({
            "paypal_account": {"token": "1234", "default": False}
        })

        self.assertEqual(PayPalAccount, paypal_account.__class__)
        self.assertEqual("1234", paypal_account.token)
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

        self.assertEqual(UnknownPaymentMethod, unknown_payment_method.__class__)
        self.assertEqual("1234", unknown_payment_method.token)
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
            "paypal_refresh_token",
            "paypal_vault_without_upgrade",
            "token",
            {
                "billing_address": Address.create_signature()},
            {
                "options": [
                    "fail_on_duplicate_payment_method",
                    "make_default",
                    "verification_merchant_account_id",
                    "verify_card",
                    "verification_amount",
                    {
                        "adyen":[
                            "overwrite_brand",
                            "selected_brand"
                        ]
                    },
                    {
                        "paypal":[
                            "payee_email",
                            "order_id",
                            "custom_field",
                            "description",
                            "amount",
                        ]
                    },
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
                    "verification_amount",
                    "verification_merchant_account_id",
                    "venmo_sdk_session",
                    {
                        "adyen":[
                            "overwrite_brand",
                            "selected_brand"
                        ]
                    }
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
        options = { "include_billing_postal_code": True }
        with self.assertRaises(ValueError):
            payment_method_gateway.grant("", options)

        with self.assertRaises(ValueError):
            payment_method_gateway.grant("\t", False)

        with self.assertRaises(ValueError):
            payment_method_gateway.grant(None, True)

    def test_nonce_revoke_params(self):
        payment_method_gateway = PaymentMethodGateway(BraintreeGateway(None))
        with self.assertRaises(ValueError):
            payment_method_gateway.revoke("")

        with self.assertRaises(ValueError):
            payment_method_gateway.revoke("\t")

        with self.assertRaises(ValueError):
            payment_method_gateway.revoke(None)

    def test_delete_with_revoke_all_grants_value_as_true(self):
        payment_method_gateway, http_mock  = self.setup_payment_method_gateway_and_mock_http()
        payment_method_gateway.delete("some_token", {"revoke_all_grants": True})
        self.assertTrue("delete('/merchants/integration_merchant_id/payment_methods/any/some_token?revoke_all_grants=true')" in str(http_mock.mock_calls))

    def test_delete_with_revoke_all_grants_value_as_false(self):
        payment_method_gateway, http_mock  = self.setup_payment_method_gateway_and_mock_http()
        payment_method_gateway.delete("some_token", {"revoke_all_grants": False})
        self.assertTrue("delete('/merchants/integration_merchant_id/payment_methods/any/some_token?revoke_all_grants=false')" in str(http_mock.mock_calls))

    def test_delete_without_revoke_all_grants(self):
        payment_method_gateway, http_mock  = self.setup_payment_method_gateway_and_mock_http()
        payment_method_gateway.delete("some_token")
        self.assertTrue("delete('/merchants/integration_merchant_id/payment_methods/any/some_token')" in str(http_mock.mock_calls)) 

    def test_delete_with_invalid_keys_to_raise_error(self):
        payment_method_gateway, http_mock  = self.setup_payment_method_gateway_and_mock_http()
        with self.assertRaises(KeyError):
            payment_method_gateway.delete("some_token", {"invalid_keys": False})

    def setup_payment_method_gateway_and_mock_http(self):
        braintree_gateway = BraintreeGateway(Configuration.instantiate())
        payment_method_gateway = PaymentMethodGateway(braintree_gateway)
        http_mock = MagicMock(name='config.http.delete')
        braintree_gateway.config.http = http_mock
        return payment_method_gateway, http_mock
