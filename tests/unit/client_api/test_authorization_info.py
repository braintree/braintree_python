import json
from tests.test_helper import *

class TestAuthorizationInfo(unittest.TestCase):
    def test_fingerprint_contains_required_data(self):
        auth_info = json.loads(AuthorizationInfo.generate())
        fingerprint = auth_info["fingerprint"]
        signature, encoded_data = fingerprint.split("|")

        self.assertTrue(len(signature) > 1)
        self.assertTrue("public_key=%s" % Configuration.public_key in encoded_data)
        self.assertTrue("created_at=" in encoded_data)

        port = os.getenv("GATEWAY_PORT") or "3000"
        client_api_url = "http://localhost:%s/merchants/%s/client_api" % (port, Configuration.merchant_id)

        self.assertEqual(auth_info["client_api_url"], client_api_url)
        self.assertEqual(auth_info["auth_url"], "http://auth.venmo.dev:4567")

    def test_fingerprint_optionally_contains_customer_id(self):
        auth_info = AuthorizationInfo.generate({
            "customer_id": "1234"
        })
        fingerprint = json.loads(auth_info)["fingerprint"]
        signature, encoded_data = fingerprint.split("|")

        self.assertTrue(len(signature) > 1)
        self.assertTrue("customer_id=1234" in encoded_data)

    def test_required_data_cannot_be_overridden(self):
        auth_info = AuthorizationInfo.generate({
            "merchant_id": "1234"
        })
        fingerprint = json.loads(auth_info)["fingerprint"]
        signature, encoded_data = fingerprint.split("|")

        self.assertTrue(len(signature) > 1)
        self.assertFalse("merchant_id=1234" in encoded_data)

    def test_credit_card_options_require_customer_id(self):
        for option in ["verify_card", "make_default", "fail_on_duplicate_payment_method"]:
            try:
                fingerprint = AuthorizationInfo.generate({
                    option: True
                })
                self.assertTrue(False, "Should have raised an exception")
            except InvalidSignatureError, e:
                self.assertTrue(str(e).find(option))
