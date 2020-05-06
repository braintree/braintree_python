import braintree
from braintree.customer import Customer
from braintree.error_result import ErrorResult
from braintree.exceptions.not_found_error import NotFoundError
from braintree.ids_search import IdsSearch
from braintree.resource import Resource
from braintree.resource_collection import ResourceCollection
from braintree.successful_result import SuccessfulResult


class CustomerGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def all(self):
        response = self.config.http().post(self.config.base_merchant_path() + "/customers/advanced_search_ids")
        return ResourceCollection({}, response, self.__fetch)

    def create(self, params=None):
        if params is None:
            params = {}
        Resource.verify_keys(params, Customer.create_signature())
        return self._post("/customers", {"customer": params})

    def delete(self, customer_id):
        self.config.http().delete(self.config.base_merchant_path() + "/customers/" + customer_id)
        return SuccessfulResult()

    def find(self, customer_id, association_filter_id=None):
        try:
            if customer_id is None or customer_id.strip() == "":
                raise NotFoundError()

            query_params = ""
            if association_filter_id:
                query_params = "?association_filter_id=" + association_filter_id

            response = self.config.http().get(self.config.base_merchant_path() + "/customers/" + customer_id + query_params)
            return Customer(self.gateway, response["customer"])
        except NotFoundError:
            raise NotFoundError("customer with id " + repr(customer_id) + " not found")

    def search(self, *query):
        if isinstance(query[0], list):
            query = query[0]

        response = self.config.http().post(self.config.base_merchant_path() + "/customers/advanced_search_ids", {"search": self.__criteria(query)})
        return ResourceCollection(query, response, self.__fetch)

    def update(self, customer_id, params=None):
        if params is None:
            params = {}
        Resource.verify_keys(params, Customer.update_signature())
        response = self.config.http().put(self.config.base_merchant_path() + "/customers/" + customer_id, {"customer": params})
        if "customer" in response:
            return SuccessfulResult({"customer": Customer(self.gateway, response["customer"])})
        elif "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])

    def __criteria(self, query):
        criteria = {}
        for term in query:
            if criteria.get(term.name):
                criteria[term.name] = dict(list(criteria[term.name].items()) + list(term.to_param().items()))
            else:
                criteria[term.name] = term.to_param()
        return criteria

    def __fetch(self, query, ids):
        criteria = self.__criteria(query)
        criteria["ids"] = braintree.customer_search.CustomerSearch.ids.in_list(ids).to_param()
        response = self.config.http().post(self.config.base_merchant_path() + "/customers/advanced_search", {"search": criteria})
        return [Customer(self.gateway, item) for item in ResourceCollection._extract_as_array(response["customers"], "customer")]

    def _post(self, url, params=None):
        if params is None:
            params = {}
        response = self.config.http().post(self.config.base_merchant_path() + url, params)
        if "customer" in response:
            return SuccessfulResult({"customer": Customer(self.gateway, response["customer"])})
        elif "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])
        else:
            pass

