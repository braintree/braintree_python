from tests.test_helper import *

class TestAuthorizationFingerprint(unittest.TestCase):
    def test_fingerprint_contains_required_data(self):
        fingerprint = AuthorizationFingerprint.generate()
        signature, encoded_data = fingerprint.split("|")

        self.assertTrue(len(signature) > 1)
        self.assertTrue("merchant_id=%s" % Configuration.merchant_id in encoded_data)
        self.assertTrue("public_key=%s" % Configuration.public_key in encoded_data)
        self.assertTrue("created_at=" in encoded_data)

    def test_fingerprint_optionally_contains_customer_id(self):
        fingerprint = AuthorizationFingerprint.generate({
            "customer_id": "1234"
        })
        signature, encoded_data = fingerprint.split("|")

        self.assertTrue(len(signature) > 1)
        self.assertTrue("customer_id=1234" in encoded_data)

    def test_required_data_cannot_be_overridden(self):
        fingerprint = AuthorizationFingerprint.generate({
            "merchant_id": "1234"
        })
        signature, encoded_data = fingerprint.split("|")

        self.assertTrue(len(signature) > 1)
        self.assertFalse("merchant_id=1234" in encoded_data)
