from tests.test_helper import *

class TestPaymentMethodNonce(unittest.TestCase):
    def test_finding_empty_id_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            PaymentMethodNonce.find(" ")

    def test_finding_None_id_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            PaymentMethodNonce.find(None)
