import unittest
import tests.test_helper
from braintree.util.crypto import Crypto
from braintree.configuration import Configuration
from braintree.transparent_redirect import TransparentRedirect

class TestTransparentRedirect(unittest.TestCase):
    def test_tr_data(self):
        data = TransparentRedirect.tr_data({"key": "val"}, "http://example.com/path?foo=bar")
        self.__assert_valid_tr_data(data)

    def __assert_valid_tr_data(self, data):
        hash, content = data.split("|", 1)
        self.assertEquals(hash, Crypto.hmac_hash(Configuration.private_key, content))

