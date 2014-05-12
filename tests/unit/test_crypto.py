from tests.test_helper import *

class TestCrypto(unittest.TestCase):
    def test_sha1_hmac_hash(self):
        actual = Crypto.sha1_hmac_hash("secretKey", "hello world")
        self.assertEquals("d503d7a1a6adba1e6474e9ff2c4167f9dfdf4247", actual)

    def test_sha256_hmac_hash(self):
        actual = Crypto.sha256_hmac_hash("secret-key", "secret-message")
        self.assertEquals("68e7f2ecab71db67b1aca2a638f5122810315c3013f27c2196cd53e88709eecc", actual)

    def test_secure_compare_returns_true_when_same(self):
        self.assertTrue(Crypto.secure_compare("a_string", "a_string"))

    def test_secure_compare_returns_false_when_different_lengths(self):
        self.assertFalse(Crypto.secure_compare("a_string", "a_string_that_is_longer"))

    def test_secure_compare_returns_false_when_different(self):
        self.assertFalse(Crypto.secure_compare("a_string", "a_strong"))
