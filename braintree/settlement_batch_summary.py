from braintree.util.http import Http
import braintree
import warnings
from braintree.exceptions.not_found_error import NotFoundError
from braintree.resource_collection import ResourceCollection
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.resource import Resource
from braintree.configuration import Configuration

class SettlementBatchSummary(Resource):
    @staticmethod
    def generate(settlement_date):
        return Configuration.gateway().settlement_batch_summary.generate(settlement_date)

    def __init__(self, gateway, attributes):
        self.records = []
