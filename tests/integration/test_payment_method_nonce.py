from tests.test_helper import *

class TestPaymentMethodNonce(unittest.TestCase):
    def test_create_nonce_from_payment_method(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "customer_id": customer_id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
        })

        result = PaymentMethodNonce.create(credit_card_result.credit_card.token)

        self.assertTrue(result.is_success)
        self.assertNotEqual(None, result.payment_method_nonce)
        self.assertNotEqual(None, result.payment_method_nonce.nonce)

    def test_create_raises_not_found_when_404(self):
        self.assertRaises(NotFoundError, PaymentMethodNonce.create, "not-a-token")

    def test_find_nonce_shows_details(self):
        nonce = PaymentMethodNonce.find("threedsecurednonce")
        three_d_secure_info = nonce.three_d_secure_info

        self.assertEquals("CreditCard", nonce.type)
        self.assertEquals("threedsecurednonce", nonce.nonce)
        self.assertEquals("Y", three_d_secure_info.enrolled)
        self.assertEquals("authenticate_successful", three_d_secure_info.status)
        self.assertEquals(True, three_d_secure_info.liability_shifted)
        self.assertEquals(True, three_d_secure_info.liability_shift_possible)

    def test_exposes_null_3ds_info_if_none_exists(self):
        http = ClientApiHttp.create()

        _, nonce = http.get_paypal_nonce({
            "consent-code": "consent-code",
            "access-token": "access-token",
            "options": {"validate": False}
        })

        found_nonce = PaymentMethodNonce.find(nonce)

        self.assertEquals(nonce, found_nonce.nonce)
        self.assertEquals(None, found_nonce.three_d_secure_info)

    def test_find_raises_not_found_when_404(self):
        self.assertRaises(NotFoundError, PaymentMethodNonce.find, "not-a-nonce")
