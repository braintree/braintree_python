import re
from braintree.util.http import Http
from braintree.exceptions.not_found_error import NotFoundError
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.resource import Resource

class Address(Resource):
    @staticmethod
    def create(params={}):
        Resource.verify_keys(params, Address.create_signature())
        if not "customer_id" in params:
            raise KeyError("customer_id must be provided")
        if not re.search("\A[0-9A-Za-z_-]+\Z", params["customer_id"]):
            raise KeyError("customer_id contains invalid characters")

        response = Http().post("/customers/" + params.pop("customer_id") + "/addresses", {"address": params})
        if "address" in response:
            return SuccessfulResult({"address": Address(response["address"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    @staticmethod
    def delete(customer_id, address_id):
        Http().delete("/customers/" + customer_id + "/addresses/" + address_id)
        return SuccessfulResult()

    @staticmethod
    def find(customer_id, address_id):
        try:
            response = Http().get("/customers/" + customer_id + "/addresses/" + address_id)
            return Address(response["address"])
        except NotFoundError:
            raise NotFoundError("address for customer " + customer_id + " with id " + address_id + " not found")

    @staticmethod
    def update(customer_id, address_id, params={}):
        Resource.verify_keys(params, Address.update_signature())
        response = Http().put(
            "/customers/" + customer_id + "/addresses/" + address_id,
            {"address": params}
        )
        if "address" in response:
            return SuccessfulResult({"address": Address(response["address"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    @staticmethod
    def create_signature():
        return ["company", "country_name", "customer_id", "extended_address", "first_name",
                "last_name", "locality", "postal_code", "region", "street_address"]

    @staticmethod
    def update_signature():
        return Address.create_signature()
