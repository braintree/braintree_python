from tests.test_helper import *
from unittest.mock import MagicMock

class TestTestingGateway(unittest.TestCase):
    def test_settle_transaction_traversal_id_raises_not_found_exception_without_calling_http(self):
        testing_gateway, http_mock = self.setup_testing_gateway_and_mock_http()
        with self.assertRaisesRegex(NotFoundError, "transaction with id '\\.\\./\\.\\./foo' not found"):
            testing_gateway.settle_transaction("../../foo")
        self.assertFalse(http_mock.called)

    def test_settlement_confirm_transaction_traversal_id_raises_not_found_exception_without_calling_http(self):
        testing_gateway, http_mock = self.setup_testing_gateway_and_mock_http()
        with self.assertRaisesRegex(NotFoundError, "transaction with id '\\.\\./\\.\\./foo' not found"):
            testing_gateway.settlement_confirm_transaction("../../foo")
        self.assertFalse(http_mock.called)

    def test_settlement_decline_transaction_traversal_id_raises_not_found_exception_without_calling_http(self):
        testing_gateway, http_mock = self.setup_testing_gateway_and_mock_http()
        with self.assertRaisesRegex(NotFoundError, "transaction with id '\\.\\./\\.\\./foo' not found"):
            testing_gateway.settlement_decline_transaction("../../foo")
        self.assertFalse(http_mock.called)

    def test_settlement_pending_transaction_traversal_id_raises_not_found_exception_without_calling_http(self):
        testing_gateway, http_mock = self.setup_testing_gateway_and_mock_http()
        with self.assertRaisesRegex(NotFoundError, "transaction with id '\\.\\./\\.\\./foo' not found"):
            testing_gateway.settlement_pending_transaction("../../foo")
        self.assertFalse(http_mock.called)

    def test_make_past_due_traversal_id_raises_not_found_exception_without_calling_http(self):
        testing_gateway, http_mock = self.setup_testing_gateway_and_mock_http()
        with self.assertRaisesRegex(NotFoundError, "subscription with id '\\.\\./\\.\\./foo' not found"):
            testing_gateway.make_past_due("../../foo")
        self.assertFalse(http_mock.called)

    def test_create_3ds_verification_traversal_id_raises_not_found_exception_without_calling_http(self):
        testing_gateway, http_mock = self.setup_testing_gateway_and_mock_http()
        with self.assertRaisesRegex(NotFoundError, "merchant account with id '\\.\\./\\.\\./foo' not found"):
            testing_gateway.create_3ds_verification("../../foo", {})
        self.assertFalse(http_mock.called)

    def setup_testing_gateway_and_mock_http(self):
        braintree_gateway = BraintreeGateway(Configuration.instantiate())
        testing_gateway = TestingGateway(braintree_gateway)
        http_mock = MagicMock(name='config.http')
        braintree_gateway.config.http = http_mock
        return testing_gateway, http_mock
