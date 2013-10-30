from tests.test_helper import *

class TestPartnerMerchant(unittest.TestCase):
    def test_representation(self):
        merchant = PartnerMerchant(None, {"partner_merchant_id": "abc123",
                                          "private_key": "my_private_key",
                                          "public_key": "my_public_key",
                                          "merchant_public_id": "foobar",
                                          "client_side_encryption_key": "cse_key"})
        self.assertTrue("partner_merchant_id: 'abc123'" in repr(merchant))
        self.assertTrue("public_key: 'my_public_key'" in repr(merchant))
        self.assertTrue("merchant_public_id: 'foobar'" in repr(merchant))
        self.assertTrue("client_side_encryption_key: 'cse_key'" in repr(merchant))

        self.assertFalse("private_key: 'my_private_key'" in repr(merchant))
