from tests.test_helper import *

class TestCreditCard(unittest.TestCase):
    def test_create_raises_exception_with_bad_keys(self):
        try:
            CreditCard.create({"bad_key": "value"})
            self.assertTrue(False)
        except KeyError, e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_update_raises_exception_with_bad_keys(self):
        try:
            CreditCard.update("token", {"bad_key": "value"})
            self.assertTrue(False)
        except KeyError, e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_tr_data_for_create_raises_error_with_bad_keys(self):
        try:
            CreditCard.tr_data_for_create({"bad_key": "value"}, "http://example.com")
            self.assertTrue(False)
        except KeyError, e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_tr_data_for_update_raises_error_with_bad_keys(self):
        try:
            CreditCard.tr_data_for_update({"bad_key": "value"}, "http://example.com")
            self.assertTrue(False)
        except KeyError, e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

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
        expected = ["billing_address_id", "cardholder_name", "cvv", "expiration_date", "expiration_month", "expiration_year", "number", "token",
            {
                "billing_address": [
                    "company", "country_code_alpha2", "country_code_alpha3", "country_code_numeric", "country_name",
                    "extended_address", "first_name", "last_name", "locality", "postal_code", "region", "street_address"
                ]
            },
            {"options": ["make_default", "verification_merchant_account_id", "verify_card"]},
            "customer_id"
        ]
        self.assertEquals(expected, CreditCard.create_signature())

    def test_update_signature(self):
        expected = ["billing_address_id", "cardholder_name", "cvv", "expiration_date", "expiration_month", "expiration_year", "number", "token",
            {
                "billing_address": [
                    "company", "country_code_alpha2", "country_code_alpha3", "country_code_numeric", "country_name",
                    "extended_address", "first_name", "last_name", "locality", "postal_code", "region", "street_address",
                    {"options": ["update_existing"]}
                ]
            },
            {"options": ["make_default", "verification_merchant_account_id", "verify_card"]}
        ]
        self.assertEquals(expected, CreditCard.update_signature())
