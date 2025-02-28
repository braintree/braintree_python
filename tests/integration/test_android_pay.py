from tests.test_helper import *

class TestAndroidPay(unittest.TestCase):
    @staticmethod
    def get_gateway():
        config = Configuration("development", "integration_merchant_id",
                               public_key="integration_public_key",
                               private_key="integration_private_key")
        return BraintreeGateway(config)
    
    def test_prepaid_reloadable(self):
        customer = Customer.create().customer
        result = PaymentMethod.create({
            "customer_id": customer.id,
            "payment_method_nonce": Nonces.AndroidPayCardVisa
        })

        self.assertTrue(result.is_success)

        android_pay_card = result.payment_method
        self.assertIsNotNone(android_pay_card.prepaid_reloadable)

        customer = Customer.find(customer.id)
        self.assertEqual(len(customer.android_pay_cards), 1)
        self.assertEqual(result.payment_method.token, customer.android_pay_cards[0].token)
