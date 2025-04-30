import warnings
from braintree.error_result import ErrorResult
from braintree.merchant_account import MerchantAccount
from braintree.paginated_collection import PaginatedCollection
from braintree.paginated_result import PaginatedResult
from braintree.resource import Resource
from braintree.resource_collection import ResourceCollection
from braintree.successful_result import SuccessfulResult
from braintree.exceptions.not_found_error import NotFoundError

class MerchantAccountGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def find(self, merchant_account_id):
        try:
            if merchant_account_id is None or merchant_account_id.strip() == "":
                raise NotFoundError()
            response = self.config.http().get(self.config.base_merchant_path() + "/merchant_accounts/" + merchant_account_id)
            return MerchantAccount(self.gateway, response["merchant_account"])
        except NotFoundError:
            raise NotFoundError("merchant account with id " + repr(merchant_account_id) + " not found")

    def create_for_currency(self, params=None):
        if params is None:
            params = {}
        return self._post("/merchant_accounts/create_for_currency", {"merchant_account": params})

    def all(self):
        pc = PaginatedCollection(self._fetch_merchant_accounts)
        return SuccessfulResult({"merchant_accounts": pc})

    def _fetch_merchant_accounts(self, current_page):
        response = self.config.http().get(self.config.base_merchant_path() + "/merchant_accounts/?page=" + str(current_page))
        body = response["merchant_accounts"]
        merchant_accounts = [MerchantAccount(self.gateway, merchant_account) for merchant_account in ResourceCollection._extract_as_array(body, "merchant_account")]
        return PaginatedResult(body["total_items"], body["page_size"], merchant_accounts)

    def _post(self, url, params=None):
        if params is None:
            params = {}
        response = self.config.http().post(self.config.base_merchant_path() + url, params)

        if "response" in response:
            response = response["response"]

        if "merchant_account" in response:
            return SuccessfulResult({"merchant_account": MerchantAccount(self.gateway, response["merchant_account"])})
        elif "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])

    def _put(self, url, params=None):
        if params is None:
            params = {}
        response = self.config.http().put(self.config.base_merchant_path() + url, params)
        if "merchant_account" in response:
            return SuccessfulResult({"merchant_account": MerchantAccount(self.gateway, response["merchant_account"])})
        elif "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])