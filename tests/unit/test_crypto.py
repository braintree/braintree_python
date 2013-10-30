from tests.test_helper import *

class TestCrypto(unittest.TestCase):
    def test_hmac_hash(self):
        actual = Crypto.hmac_hash(b"secretKey", b"hello world");
        self.assertEquals("d503d7a1a6adba1e6474e9ff2c4167f9dfdf4247", actual);

