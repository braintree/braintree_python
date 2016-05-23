from tests.test_helper import *
import datetime
import braintree.test.venmo_sdk as venmo_sdk

class TestCreditCard(unittest.TestCase):
    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_create_raises_exception_with_bad_keys(self):
        CreditCard.create({"bad_key": "value"})

    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_update_raises_exception_with_bad_keys(self):
        CreditCard.update("token", {"bad_key": "value"})

    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_tr_data_for_create_raises_error_with_bad_keys(self):
        CreditCard.tr_data_for_create({"bad_key": "value"}, "http://example.com")

    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_tr_data_for_update_raises_error_with_bad_keys(self):
        CreditCard.tr_data_for_update({"bad_key": "value"}, "http://example.com")

    def test_transparent_redirect_create_url(self):
        port = os.getenv("GATEWAY_PORT") or "3000"
        self.assertEquals(
            "http://localhost:" + port + "/merchants/integration_merchant_id/payment_methods/all/create_via_transparent_redirect_request",
            CreditCard.transparent_redirect_create_url()
        )

    def test_transparent_redirect_update_url(self):
        port = os.getenv("GATEWAY_PORT") or "3000"
        self.assertEquals(
            "http://localhost:" + port + "/merchants/integration_merchant_id/payment_methods/all/update_via_transparent_redirect_request",
            CreditCard.transparent_redirect_update_url()
        )

    @raises(DownForMaintenanceError)
    def test_confirm_transaprant_redirect_raises_error_given_503_status_in_query_string(self):
        CreditCard.confirm_transparent_redirect(
            "http_status=503&id=6kdj469tw7yck32j&hash=1b3d29199a282e63074a7823b76bccacdf732da6"
        )

    def test_create_signature(self):
        expected = ["billing_address_id", "cardholder_name", "cvv", "expiration_date", "expiration_month",
            "expiration_year", "device_session_id", "fraud_merchant_id", "number", "token", "venmo_sdk_payment_method_code",
            "device_data", "payment_method_nonce",
            {
                "billing_address": [
                    "company", "country_code_alpha2", "country_code_alpha3", "country_code_numeric", "country_name",
                    "extended_address", "first_name", "last_name", "locality", "postal_code", "region", "street_address"
                ]
            },
            {"options": ["make_default", "verification_merchant_account_id", "verify_card", "verification_amount", "venmo_sdk_session", "fail_on_duplicate_payment_method"]},
            "customer_id"
        ]
        self.assertEquals(expected, CreditCard.create_signature())

    def test_update_signature(self):
        expected = ["billing_address_id", "cardholder_name", "cvv", "expiration_date", "expiration_month",
            "expiration_year", "device_session_id", "fraud_merchant_id", "number", "token", "venmo_sdk_payment_method_code",
            "device_data", "payment_method_nonce",
            {
                "billing_address": [
                    "company", "country_code_alpha2", "country_code_alpha3", "country_code_numeric", "country_name",
                    "extended_address", "first_name", "last_name", "locality", "postal_code", "region", "street_address",
                    {"options": ["update_existing"]}
                ]
            },
            {"options": ["make_default", "verification_merchant_account_id", "verify_card", "verification_amount", "venmo_sdk_session"]}
        ]
        self.assertEquals(expected, CreditCard.update_signature())

    @raises(NotFoundError)
    def test_finding_empty_id_raises_not_found_exception(self):
        CreditCard.find(" ")

    @raises(NotFoundError)
    def test_finding_none_raises_not_found_exception(self):
        CreditCard.find(None)

    def test_multiple_verifications_sort(self):
        verification1 = {"created_at": datetime.datetime(2014, 11, 18, 23, 20, 20), "id":123}
        verification2 = {"created_at": datetime.datetime(2014, 11, 18, 23, 20, 21), "id":456}
        credit_card = CreditCard(Configuration.gateway(), {"verifications": [verification1, verification2]})
        self.assertEquals(credit_card.verification.id, 456)
