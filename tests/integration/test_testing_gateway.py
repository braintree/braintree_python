from tests.test_helper import *
from braintree.configuration import Configuration
from braintree.exceptions.test_operation_performed_in_production_error import TestOperationPerformedInProductionError

class TestTestingGateway(unittest.TestCase):
    def setUp(self):
        config = Configuration(braintree.Environment.Production, "", "", "")
        braintree_gateway = BraintreeGateway(config)
        self.gateway = TestingGateway(braintree_gateway)

    @raises(TestOperationPerformedInProductionError)
    def test_error_is_raised_in_production_for_settle_transaction(self):
        self.gateway.settle_transaction("")

    @raises(TestOperationPerformedInProductionError)
    def test_error_is_raised_in_production_for_make_past_due(self):
        self.gateway.make_past_due("")

    @raises(TestOperationPerformedInProductionError)
    def test_error_is_raised_in_production_for_escrow_transaction(self):
        self.gateway.escrow_transaction("")

    @raises(TestOperationPerformedInProductionError)
    def test_error_is_raised_in_production_for_settlement_confirm_transaction(self):
        self.gateway.settlement_confirm_transaction("")

    @raises(TestOperationPerformedInProductionError)
    def test_error_is_raised_in_production_for_settlement_decline_transaction(self):
        self.gateway.settlement_decline_transaction("")

    @raises(TestOperationPerformedInProductionError)
    def test_error_is_raised_in_production_for_create_3ds_verification(self):
        self.gateway.create_3ds_verification("", "")

    @raises(TestOperationPerformedInProductionError)
    def test_error_is_raised_in_production(self):
        self.gateway.settle_transaction("")
