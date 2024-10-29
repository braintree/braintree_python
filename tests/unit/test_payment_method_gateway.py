from tests.test_helper import *
from braintree.payment_method_gateway import PaymentMethodGateway
from unittest.mock import MagicMock

class TestPaymentMethodGateway(unittest.TestCase):
    def test_create_signature(self):
        actual_signature = PaymentMethod.signature("create")

        expected_signature = [
            "billing_address_id",
            "cardholder_name",
            "customer_id",
            "cvv",
            "device_data",
            "expiration_date",
            "expiration_month",
            "expiration_year",
            "number",
            "payment_method_nonce",
            "paypal_refresh_token",
            "token",
            "device_session_id",
            {
                "billing_address": Address.create_signature()},
            {
                "options": [
                    "fail_on_duplicate_payment_method",
                    "fail_on_duplicate_payment_method_for_customer",
                    "make_default",
                    "skip_advanced_fraud_checking",
                    "us_bank_account_verification_method",
                    "verification_account_type",
                    "verification_add_ons",
                    "verification_amount",
                    "verification_merchant_account_id",
                    "verify_card",
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
                            {
                                "shipping":[
                                    "company",
                                    "country_code_alpha2",
                                    "country_code_alpha3",
                                    "country_code_numeric",
                                    "country_name",
                                    "customer_id",
                                    "extended_address",
                                    "first_name",
                                    {"international_phone": ["country_code", "national_number"]},
                                    "last_name",
                                    "locality",
                                    "phone_number",
                                    "postal_code",
                                    "region",
                                    "street_address",
                                ]
                            },
                        ]
                    },
                ]
            },
            {
                "three_d_secure_pass_thru": [
                    "cavv",
                    "ds_transaction_id",
                    "eci_flag",
                    "three_d_secure_version",
                    "xid"
                    ]
            },
        ]

        self.assertEqual(expected_signature, actual_signature)

    def test_update_signature(self):
        actual_signature = PaymentMethod.update_signature()

        expected_signature = [
            "billing_address_id",
            "cardholder_name",
            "cvv",
            "device_data",
            "expiration_date",
            "expiration_month",
            "expiration_year",
            "number",
            "payment_method_nonce",
            "token",
            "venmo_sdk_payment_method_code",  # NEXT_MJOR_VERSION remove venmo_sdk_payment_method_code
            "device_session_id",
            "fraud_merchant_id",
            {
                "options": [
                    "fail_on_duplicate_payment_method_for_customer",
                    "make_default",
                    "skip_advanced_fraud_checking",
                    "us_bank_account_verification_method",
                    "venmo_sdk_session", # NEXT_MJOR_VERSION remove venmo_sdk_session
                    "verification_account_type",
                    "verification_add_ons",
                    "verification_amount",
                    "verification_merchant_account_id",
                    "verify_card",
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
            },
            {
                "three_d_secure_pass_thru": [
                    "cavv",
                    "ds_transaction_id",
                    "eci_flag",
                    "three_d_secure_version",
                    "xid"
                    ]
            },
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
