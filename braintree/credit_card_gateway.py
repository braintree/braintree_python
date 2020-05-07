import braintree
from braintree.credit_card import CreditCard
from braintree.error_result import ErrorResult
from braintree.exceptions.not_found_error import NotFoundError
from braintree.ids_search import IdsSearch
from braintree.resource import Resource
from braintree.resource_collection import ResourceCollection
from braintree.successful_result import SuccessfulResult


class CreditCardGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def create(self, params=None):
        if params is None:
            params = {}
        Resource.verify_keys(params, CreditCard.create_signature())
        return self._post("/payment_methods", {"credit_card": params})

    def delete(self, credit_card_token):
        self.config.http().delete(self.config.base_merchant_path() + "/payment_methods/credit_card/" + credit_card_token)
        return SuccessfulResult()

    def expired(self):
        response = self.config.http().post(self.config.base_merchant_path() + "/payment_methods/all/expired_ids")
        return ResourceCollection(None, response, self.__fetch_expired)

    def expiring_between(self, start_date, end_date):
        formatted_start_date = start_date.strftime("%m%Y")
        formatted_end_date = end_date.strftime("%m%Y")
        query = "start=%s&end=%s" % (formatted_start_date, formatted_end_date)
        response = self.config.http().post(self.config.base_merchant_path() + "/payment_methods/all/expiring_ids?" + query)
        return ResourceCollection(query, response, self.__fetch_existing_between)

    def find(self, credit_card_token):
        try:
            if credit_card_token is None or credit_card_token.strip() == "":
                raise NotFoundError()
            response = self.config.http().get(self.config.base_merchant_path() + "/payment_methods/credit_card/" + credit_card_token)
            return CreditCard(self.gateway, response["credit_card"])
        except NotFoundError:
            raise NotFoundError("payment method with token " + repr(credit_card_token) + " not found")

    def forward(self, credit_card_token, receiving_merchant_id):
        raise NotFoundError("This method of forwarding payment methods is no longer supported. Please consider the Grant API for similar functionality.")

    def from_nonce(self, nonce):
        try:
            if nonce is None or nonce.strip() == "":
                raise NotFoundError()
            response = self.config.http().get(self.config.base_merchant_path() + "/payment_methods/from_nonce/" + nonce)
            return CreditCard(self.gateway, response["credit_card"])
        except NotFoundError:
            raise NotFoundError("payment method with nonce " + repr(nonce) + " locked, consumed or not found")

    def update(self, credit_card_token, params=None):
        if params is None:
            params = {}
        Resource.verify_keys(params, CreditCard.update_signature())
        response = self.config.http().put(self.config.base_merchant_path() + "/payment_methods/credit_card/" + credit_card_token, {"credit_card": params})
        if "credit_card" in response:
            return SuccessfulResult({"credit_card": CreditCard(self.gateway, response["credit_card"])})
        elif "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])

    def __fetch_expired(self, query, ids):
        criteria = {}
        criteria["ids"] = IdsSearch.ids.in_list(ids).to_param()
        response = self.config.http().post(self.config.base_merchant_path() + "/payment_methods/all/expired", {"search": criteria})
        return [CreditCard(self.gateway, item) for item in ResourceCollection._extract_as_array(response["payment_methods"], "credit_card")]

    def __fetch_existing_between(self, query, ids):
        criteria = {}
        criteria["ids"] = IdsSearch.ids.in_list(ids).to_param()
        response = self.config.http().post(self.config.base_merchant_path() + "/payment_methods/all/expiring?" + query, {"search": criteria})
        return [CreditCard(self.gateway, item) for item in ResourceCollection._extract_as_array(response["payment_methods"], "credit_card")]

    def _post(self, url, params=None):
        if params is None:
            params = {}
        response = self.config.http().post(self.config.base_merchant_path() + url, params)
        if "credit_card" in response:
            return SuccessfulResult({"credit_card": CreditCard(self.gateway, response["credit_card"])})
        elif "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])

