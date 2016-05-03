from tests.test_helper import *
from braintree.test.nonces import Nonces
import sys
if sys.version_info[0] == 2:
    import urlparse
else:
    import urllib.parse as urlparse

class TestOAuthGateway(unittest.TestCase):
    def setUp(self):
        self.gateway = BraintreeGateway(
            client_id = "client_id$development$integration_client_id",
            client_secret = "client_secret$development$integration_client_secret"
        )

    def test_create_token_from_code(self):
        code = TestHelper.create_grant(self.gateway, {
            "merchant_public_id": "integration_merchant_id",
            "scope": "read_write"
        })

        result = self.gateway.oauth.create_token_from_code({
            "code": code
        })

        self.assertTrue(result.is_success)

        credentials = result.credentials
        self.assertIsNotNone(credentials.access_token)
        self.assertIsNotNone(credentials.refresh_token)
        self.assertIsNotNone(credentials.expires_at)
        self.assertEquals("bearer", credentials.token_type)


    def test_create_token_from_code_with_bad_parameters(self):
        result = self.gateway.oauth.create_token_from_code({
            "code": "bad_code",
            "scope": "read_write"
        })

        self.assertFalse(result.is_success)
        self.assertEqual(
            result.errors.for_object("credentials").on("code")[0].code,
            ErrorCodes.OAuth.InvalidGrant
        )
        self.assertIn(result.message, "Invalid grant: code not found")

    def test_create_token_from_code_returns_helpful_error_with_bad_credentials(self):
        gateway = BraintreeGateway(
            access_token = "access_token$development$integration_merchant_id$fb27c79dd",
        )

        with self.assertRaises(ConfigurationError) as error:
            result = gateway.oauth.create_token_from_code({
                "code": "some_code",
                "scope": "read_write"
            })

        config_error = error.exception
        self.assertIn("client_id and client_secret are required", str(config_error))

    def test_create_token_from_refresh_token(self):
        code = TestHelper.create_grant(self.gateway, {
            "merchant_public_id": "integration_merchant_id",
            "scope": "read_write"
        })

        refresh_token = self.gateway.oauth.create_token_from_code({
            "code": code,
            "scope": "read_write"
        }).credentials.refresh_token

        result = self.gateway.oauth.create_token_from_refresh_token({
            "refresh_token": refresh_token
        })

        self.assertTrue(result.is_success)

        credentials = result.credentials
        self.assertIsNotNone(credentials.access_token)
        self.assertIsNotNone(credentials.refresh_token)
        self.assertIsNotNone(credentials.expires_at)
        self.assertEquals("bearer", credentials.token_type)

    def test_revoke_access_token(self):
        code = TestHelper.create_grant(self.gateway, {
            "merchant_public_id": "integration_merchant_id",
            "scope": "read_write"
        })

        access_token = self.gateway.oauth.create_token_from_code({
            "code": code,
            "scope": "read_write"
        }).credentials.access_token

        result = self.gateway.oauth.revoke_access_token(access_token)

        self.assertTrue(result.is_success)

        with self.assertRaises(AuthenticationError) as error:
            gateway = BraintreeGateway(access_token = access_token)

            gateway.customer.create()

    def test_connect_url(self):
        connect_url = self.gateway.oauth.connect_url({
             "merchant_id": "integration_merchant_id",
             "redirect_uri": "http://bar.example.com",
             "scope": "read_write",
             "state": "baz_state",
             "landing_page": "login",
             "user": {
               "country": "USA",
               "email": "foo@example.com",
               "first_name": "Bob",
               "last_name": "Jones",
               "phone": "555-555-5555",
               "dob_year": "1970",
               "dob_month": "01",
               "dob_day": "01",
               "street_address": "222 W Merchandise Mart",
               "locality": "Chicago",
               "region": "IL",
               "postal_code": "60606"
             },
             "business": {
               "name": "14 Ladders",
               "registered_as": "14.0 Ladders",
               "industry": "Ladders",
               "description": "We sell the best ladders",
               "street_address": "111 N Canal",
               "locality": "Chicago",
               "region": "IL",
               "postal_code": "60606",
               "country": "USA",
               "annual_volume_amount": "1000000",
               "average_transaction_amount": "100",
               "maximum_transaction_amount": "10000",
               "ship_physical_goods": "true",
               "fulfillment_completed_in": 7,
               "currency": "USD",
               "website": "http://example.com"
            },
            "payment_methods": ["credit_card", "paypal"]
        })
        query_string = urlparse.urlparse(connect_url)[4]
        params = urlparse.parse_qs(query_string)

        self.assertEqual(params["merchant_id"], ["integration_merchant_id"])
        self.assertEqual(params["client_id"], ["client_id$development$integration_client_id"])
        self.assertEqual(params["redirect_uri"], ["http://bar.example.com"])
        self.assertEqual(params["scope"], ["read_write"])
        self.assertEqual(params["state"], ["baz_state"])
        self.assertEqual(params["landing_page"], ["login"])

        self.assertEqual(params["user[country]"], ["USA"])
        self.assertEqual(params["business[name]"], ["14 Ladders"])
        self.assertEqual(params["payment_methods[]"], ["credit_card", "paypal"])

        self.assertEqual(len(params["signature"][0]), 64)
        self.assertEqual(params["algorithm"], ["SHA256"])

    def test_connect_url_limits_payment_methods(self):
        connect_url = self.gateway.oauth.connect_url({
             "merchant_id": "integration_merchant_id",
             "redirect_uri": "http://bar.example.com",
             "scope": "read_write",
             "state": "baz_state",
            "payment_methods": ["credit_card"]
        })
        query_string = urlparse.urlparse(connect_url)[4]
        params = urlparse.parse_qs(query_string)

        self.assertEqual(params["merchant_id"], ["integration_merchant_id"])
        self.assertEqual(params["client_id"], ["client_id$development$integration_client_id"])
        self.assertEqual(params["redirect_uri"], ["http://bar.example.com"])
        self.assertEqual(params["payment_methods[]"], ["credit_card"])

    def test_compute_signature(self):
        url = "http://localhost:3000/oauth/connect?business%5Bname%5D=We+Like+Spaces&client_id=client_id%24development%24integration_client_id"

        signature = self.gateway.oauth._compute_signature(url)
        self.assertEqual(signature, "a36bcf10dd982e2e47e0d6a2cb930aea47ade73f954b7d59c58dae6167894d41")
