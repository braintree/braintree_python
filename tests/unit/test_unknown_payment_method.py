from tests.test_helper import *

class TestUnknownPaymentMethod(unittest.TestCase):
    def test_image_url(self):
        unknown_payment_method = UnknownPaymentMethod("gateway", {"token": "TOKEN"})
        self.assertEquals("https://assets.braintreegateway.com/payment_method_logo/unknown.png", unknown_payment_method.image_url())
