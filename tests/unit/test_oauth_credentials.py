from tests.test_helper import *
from braintree.oauth_credentials import OAuthCredentials

class TestOAuthCredentials(unittest.TestCase):
    def test_representation_does_not_leak_tokens_through_successful_result(self):
        credentials = OAuthCredentials(None, {"access_token": "access_token$fake$secret",
                                              "refresh_token": "refresh_token$fake$secret",
                                              "token_type": "bearer",
                                              "expires_at": "2024-01-01T00:00:00Z",
                                              "scope": "read_write"})
        self.assertTrue("token_type: 'bearer'" in repr(credentials))
        self.assertTrue("expires_at: '2024-01-01T00:00:00Z'" in repr(credentials))
        self.assertTrue("scope: 'read_write'" in repr(credentials))

        self.assertFalse("access_token" in repr(credentials))
        self.assertFalse("refresh_token" in repr(credentials))
