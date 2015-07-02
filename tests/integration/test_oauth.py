from tests.test_helper import *
from braintree.test.nonces import Nonces

class TestOAuthGateway(unittest.TestCase):
    def test_create_token_from_code(self):
        gateway = BraintreeGateway(
            client_id = "client_id$development$integration_client_id",
            client_secret = "client_secret$development$integration_client_secret",
            environment = Environment.Development
        )

        code = TestHelper.create_grant(gateway, {
            "merchant_public_id": "integration_merchant_id",
            "scope": "read_write"
        })

        result = gateway.oauth.create_token_from_code({
            "code": code
        })

        self.assertTrue(result.is_success)

        credentials = result.credentials
        self.assertIsNotNone(credentials.access_token)
        self.assertIsNotNone(credentials.refresh_token)
        self.assertIsNotNone(credentials.expires_at)
        self.assertEquals("bearer", credentials.token_type)
