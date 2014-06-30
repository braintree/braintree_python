import json
from tests.test_helper import *

class TestClientToken(unittest.TestCase):
    def test_credit_card_options_require_customer_id(self):
        for option in ["verify_card", "make_default", "fail_on_duplicate_payment_method"]:
            try:
                client_token = ClientToken.generate({
                    "options": {option: True}
                })
                self.assertTrue(False, "Should have raised an exception")
            except InvalidSignatureError as e:
                self.assertTrue(str(e).find(option))

    def test_generate_delegates_client_token_generation_to_gateway(self):
        class MockGateway():
            def generate(self, _):
                return "mock_client_token"

        mock_gateway = MockGateway()
        client_token = ClientToken.generate({}, mock_gateway)

        self.assertEqual("mock_client_token", client_token)
