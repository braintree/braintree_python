from tests.test_helper import *
import datetime

class TestCreditCard(unittest.TestCase):
    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_create_raises_exception_with_bad_keys(self):
        CreditCard.create({"bad_key": "value"})

    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_update_raises_exception_with_bad_keys(self):
        CreditCard.update("token", {"bad_key": "value"})

    def test_create_signature(self):
        expected = ["billing_address_id", "cardholder_name", "cvv", "expiration_date", "expiration_month",
            "expiration_year", "number", "token", "venmo_sdk_payment_method_code",
            "device_data", "payment_method_nonce",
            "device_session_id", "fraud_merchant_id",
            {
                "billing_address": [
                    "company", "country_code_alpha2", "country_code_alpha3", "country_code_numeric", "country_name",
                    "extended_address", "first_name", "last_name", "locality", "postal_code", "region", "street_address"
                ]
            },
            {"options": ["make_default", "verification_merchant_account_id", "verify_card", "verification_amount", "verification_account_type", "venmo_sdk_session", "fail_on_duplicate_payment_method", {"adyen":["overwrite_brand", "selected_brand"]}
            ]},
            {
                "three_d_secure_pass_thru": [
                    "cavv", "ds_transaction_id", "eci_flag", "three_d_secure_version", "xid"
                ]
            },
            "customer_id"
        ]
        self.assertEqual(expected, CreditCard.create_signature())

    def test_update_signature(self):
        expected = ["billing_address_id", "cardholder_name", "cvv", "expiration_date", "expiration_month",
            "expiration_year", "number", "token", "venmo_sdk_payment_method_code",
            "device_data", "payment_method_nonce",
            "device_session_id", "fraud_merchant_id",
            {
                "billing_address": [
                    "company", "country_code_alpha2", "country_code_alpha3", "country_code_numeric", "country_name",
                    "extended_address", "first_name", "last_name", "locality", "postal_code", "region", "street_address",
                    {"options": ["update_existing"]}
                ]
            },
            {"options": ["make_default", "verification_merchant_account_id", "verify_card", "verification_amount", "verification_account_type", "venmo_sdk_session", "fail_on_duplicate_payment_method", {"adyen":["overwrite_brand", "selected_brand"]}
            ]},
            {
                "three_d_secure_pass_thru": [
                    "cavv", "ds_transaction_id", "eci_flag", "three_d_secure_version", "xid"
                ]
            },
        ]
        self.assertEqual(expected, CreditCard.update_signature())

    @raises(NotFoundError)
    def test_finding_empty_id_raises_not_found_exception(self):
        CreditCard.find(" ")

    @raises(NotFoundError)
    def test_finding_none_raises_not_found_exception(self):
        CreditCard.find(None)

    @raises(NotFoundError)
    def test_from_nonce_empty_id_raises_not_found_exception(self):
        CreditCard.from_nonce(" ")

    @raises(NotFoundError)
    def test_from_nonce_none_raises_not_found_exception(self):
        CreditCard.from_nonce(None)

    def test_multiple_verifications_sort(self):
        verification1 = {"created_at": datetime.datetime(2014, 11, 18, 23, 20, 20), "id": 123, "amount": "0.00"}
        verification2 = {"created_at": datetime.datetime(2014, 11, 18, 23, 20, 21), "id": 456, "amount": "1.00"}
        credit_card = CreditCard(Configuration.gateway(), {"verifications": [verification1, verification2]})
        self.assertEqual(456, credit_card.verification.id)
        self.assertEqual(1.00, credit_card.verification.amount)
