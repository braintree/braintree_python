from tests.test_helper import *

class TestMerchantGateway(unittest.TestCase):
    def setUp(self):
        self.gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret"
        )

    # NEXT_MAJOR_VERSION remove this test
    def test_create_raises_server_error(self):
        with self.assertRaises(ServerError):
            self.gateway.merchant.create({
                "email": "name@email.com",
                "country_code_alpha3": "GBR",
                "payment_methods": ["credit_card", "paypal"]
            })
