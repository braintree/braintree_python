from tests.test_helper import *

class FakeDigest(object):

    @staticmethod
    def hmac_hash(key, data):
        return "%s_signed_with_%s" % (data, key)

class TestSignatureService(unittest.TestCase):

    def test_hashes_with_digest(self):
        signature_service = SignatureService("fake_key", FakeDigest.hmac_hash)
        signed = signature_service.sign({"foo": "bar"})
        self.assertEquals("foo=bar_signed_with_fake_key|foo=bar", signed)
