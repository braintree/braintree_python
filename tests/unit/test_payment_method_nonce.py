from tests.test_helper import *

class TestPaymentMethodNonce(unittest.TestCase):
    def test_finding_empty_id_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            PaymentMethodNonce.find(" ")

    def test_finding_None_id_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            PaymentMethodNonce.find(None)

    def test_find_traversal_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "payment method nonce with id '\\.\\./\\.\\./foo' not found"):
            PaymentMethodNonce.find("../../foo")

    def test_create_traversal_token_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "payment method with token '\\.\\./\\.\\./foo' not found"):
            PaymentMethodNonce.create("../../foo")
