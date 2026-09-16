from tests.test_helper import *
from unittest.mock import MagicMock

class TestMerchantAccountGateway(unittest.TestCase):
    def test_find_traversal_id_raises_not_found_exception_without_calling_http(self):
        merchant_account_gateway, http_mock = self.setup_merchant_account_gateway_and_mock_http()
        with self.assertRaisesRegex(NotFoundError, "merchant account with id '\\.\\./\\.\\./foo' not found"):
            merchant_account_gateway.find("../../foo")
        self.assertFalse(http_mock.called)

    def setup_merchant_account_gateway_and_mock_http(self):
        braintree_gateway = BraintreeGateway(Configuration.instantiate())
        merchant_account_gateway = MerchantAccountGateway(braintree_gateway)
        http_mock = MagicMock(name='config.http')
        braintree_gateway.config.http = http_mock
        return merchant_account_gateway, http_mock
