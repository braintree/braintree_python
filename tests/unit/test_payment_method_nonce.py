from tests.test_helper import *

class TestPaymentMethodNonce(unittest.TestCase):
    @raises(NotFoundError)
    def test_finding_empty_id_raises_not_found_exception(self):
        PaymentMethodNonce.find(" ")

    @raises(NotFoundError)
    def test_finding_None_id_raises_not_found_exception(self):
        PaymentMethodNonce.find(None)
