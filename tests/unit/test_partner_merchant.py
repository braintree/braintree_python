from tests.test_helper import *

class TestPartnerMerchant(unittest.TestCase):
    def test_representation(self):
        merchant = PartnerMerchant(None, {"partner_merchant_id": "abc123",
                                          "private_key": "my_private_key",
                                          "public_key": "my_public_key",
                                          "merchant_public_id": "foobar",
                                          "client_side_encryption_key": "cse_key"})
        self.assertTrue("<PartnerMerchant {partner_merchant_id: 'abc123', public_key: 'my_public_key', private_key: 'my_private_key', merchant_public_id: 'foobar', client_side_encryption_key: 'cse_key'} at" in repr(merchant))
