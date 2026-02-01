from tests.test_helper import *

class TestOAuthAccessRevocation(unittest.TestCase):
    def test_assigns_merchant_id(self):
        revocation = OAuthAccessRevocation({"merchant_id": "abc123xyz"})

        self.assertEqual(revocation.merchant_id, "abc123xyz")
