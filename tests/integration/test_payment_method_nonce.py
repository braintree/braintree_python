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
