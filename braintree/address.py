import re
from braintree.util.http import Http
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.resource import Resource

class Address(Resource):
    @staticmethod
    def create(params={}):
        Resource.verify_keys(params, Address.create_signature())
        if not params["customer_id"]:
            raise KeyError("customer_id must be provided")
        if not re.match("\A[0-9A-Za-z_-]+\Z", params["customer_id"]):
            raise KeyError("customer_id contains invalid charaters")

        response = Http().post("/customers/" + params.pop("customer_id") + "/addresses", {"address": params})
        if "address" in response:
            return SuccessfulResult({"address": Address(response["address"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])
        else:
            pass

    @staticmethod
    def delete(customer_id, address_id):
        response = Http().delete("/customers/" + customer_id + "/addresses/" + address_id)
        return SuccessfulResult()

    @staticmethod
    def create_signature():
        return ["company", "country_name", "customer_id", "extended_address", "first_name",
                "last_name", "locality", "postal_code", "region", "street_address"]
