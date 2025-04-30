from tests.test_helper import *
from braintree.configuration import Configuration
from braintree.exceptions.test_operation_performed_in_production_error import TestOperationPerformedInProductionError

class TestTestingGateway(unittest.TestCase):
    def setUp(self):
        config = Configuration(braintree.Environment.Production, "merchant_id", "public_key", "private_key")
        braintree_gateway = BraintreeGateway(config)
        self.gateway = TestingGateway(braintree_gateway)

    def test_error_is_raised_in_production_for_settle_transaction(self):
        with self.assertRaises(TestOperationPerformedInProductionError):
            self.gateway.settle_transaction("")

    def test_error_is_raised_in_production_for_make_past_due(self):
        with self.assertRaises(TestOperationPerformedInProductionError):
            self.gateway.make_past_due("")

    def test_error_is_raised_in_production_for_settlement_confirm_transaction(self):
        with self.assertRaises(TestOperationPerformedInProductionError):
            self.gateway.settlement_confirm_transaction("")

    def test_error_is_raised_in_production_for_settlement_decline_transaction(self):
        with self.assertRaises(TestOperationPerformedInProductionError):
            self.gateway.settlement_decline_transaction("")

    def test_error_is_raised_in_production_for_create_3ds_verification(self):
        with self.assertRaises(TestOperationPerformedInProductionError):
            self.gateway.create_3ds_verification("", "")

    def test_error_is_raised_in_production(self):
        with self.assertRaises(TestOperationPerformedInProductionError):
            self.gateway.settle_transaction("")
