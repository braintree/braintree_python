import braintree
from braintree.address import Address
from braintree.resource import Resource
from braintree.configuration import Configuration


class PaymentMethod(Resource):
    @staticmethod
    def create(params=None):
        if params is None:
            params = {}
        return Configuration.gateway().payment_method.create(params)

    @staticmethod
    def find(payment_method_token):
        return Configuration.gateway().payment_method.find(payment_method_token)

    @staticmethod
    def update(payment_method_token, params):
        return Configuration.gateway().payment_method.update(payment_method_token, params)

    @staticmethod
    def delete(payment_method_token, options=None):
        if options is None:
            options = {}
        return Configuration.gateway().payment_method.delete(payment_method_token, options)

    @staticmethod
    def create_signature():
        return PaymentMethod.signature("create")

    @staticmethod
    def signature(type):
        options = [
            "fail_on_duplicate_payment_method",
            "make_default",
            "skip_advanced_fraud_checking",
            "us_bank_account_verification_method",
            "verification_account_type",
            "verification_amount",
            "verification_merchant_account_id",
            "verify_card",
            {
                "adyen": [
                    "overwrite_brand",
                    "selected_brand"
                ]
            },
            {
                "paypal": [
                    "payee_email",
                    "order_id",
                    "custom_field",
                    "description",
                    "amount",
                    { "shipping": Address.create_signature() }
                ],
            },
        ]

        three_d_secure_pass_thru = [
            "cavv",
            "ds_transaction_id",
            "eci_flag",
            "three_d_secure_version",
            "xid"
        ]

        signature = [
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
            "device_session_id", # NEXT_MAJOR_VERSION remove device_session_id
            {
                "billing_address": Address.create_signature()
            },
            {
                "options": options
            },
            {
                "three_d_secure_pass_thru": three_d_secure_pass_thru
            }

        ]
        return signature

    @staticmethod
    def update_signature():
        three_d_secure_pass_thru = [
            "cavv",
            "ds_transaction_id",
            "eci_flag",
            "three_d_secure_version",
            "xid"
        ]

        signature = [
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
            "venmo_sdk_payment_method_code",
            "device_session_id", "fraud_merchant_id", # NEXT_MAJOR_VERSION remove device_session_id and fraud_merchant_id
            {
                "options": [
                    "make_default",
                    "skip_advanced_fraud_checking",
                    "us_bank_account_verification_method",
                    "venmo_sdk_session",
                    "verification_account_type",
                    "verification_amount",
                    "verification_merchant_account_id",
                    "verify_card",
                    {
                        "adyen": [
                            "overwrite_brand",
                            "selected_brand"
                        ]
                    }
                ]
            },
            {
                "billing_address": Address.update_signature() + [{"options": ["update_existing"]}]
            },
            {
                "three_d_secure_pass_thru": three_d_secure_pass_thru
            }
        ]
        return signature

    @staticmethod
    def delete_signature():
        return ["revoke_all_grants"]
