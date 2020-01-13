from tests.test_helper import *
from braintree.apple_pay_gateway import ApplePayGateway
if sys.version_info[0] == 2:
    from mock import MagicMock
else:
    from unittest.mock import MagicMock

class TestApplePayGateway(unittest.TestCase):
    @staticmethod
    def setup_apple_pay_gateway_and_mock_http():
        braintree_gateway = BraintreeGateway(Configuration.instantiate())
        apple_pay_gateway = ApplePayGateway(braintree_gateway)
        http_mock = MagicMock(name='config.http')
        braintree_gateway.config.http = http_mock
        return apple_pay_gateway, http_mock

    def test_registered_domains(self):
        apple_pay_gateway, http_mock = self.setup_apple_pay_gateway_and_mock_http()
        apple_pay_gateway.registered_domains()
        self.assertTrue("get('/merchants/integration_merchant_id/processing/apple_pay/registered_domains')" in str(http_mock.mock_calls))

    def test_register_domain(self):
        apple_pay_gateway, http_mock = self.setup_apple_pay_gateway_and_mock_http()
        apple_pay_gateway.register_domain('test.example.com')
        self.assertTrue("post('/merchants/integration_merchant_id/processing/apple_pay/validate_domains', {'url': 'test.example.com'})" in str(http_mock.mock_calls))

    def test_unregister_domain(self):
        apple_pay_gateway, http_mock = self.setup_apple_pay_gateway_and_mock_http()
        apple_pay_gateway.unregister_domain('test.example.com')
        self.assertTrue("delete('/merchants/integration_merchant_id/processing/apple_pay/unregister_domain?url=test.example.com')" in str(http_mock.mock_calls))
