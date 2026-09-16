import braintree
from braintree.error_result import ErrorResult
from braintree.resource import Resource
from braintree.resource_collection import ResourceCollection
from braintree.transaction_line_item import TransactionLineItem
from braintree.exceptions.not_found_error import NotFoundError
from braintree.exceptions.request_timeout_error import RequestTimeoutError
from braintree.util.validation import is_invalid_path_segment

class TransactionLineItemGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def find_all(self, transaction_id):
        try:
            if is_invalid_path_segment(transaction_id):
                raise NotFoundError()
            response = self.config.http().get(self.config.base_merchant_path() + "/transactions/" + transaction_id + "/line_items")
            if "line_items" in response:
                return [TransactionLineItem(item) for item in ResourceCollection._extract_as_array(response, "line_items")]
            else:
                raise RequestTimeoutError()
        except NotFoundError:
            raise NotFoundError("transaction line items with id " + repr(transaction_id) + " not found")
