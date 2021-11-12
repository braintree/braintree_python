import re
import braintree
from braintree.plan import Plan
from braintree.error_result import ErrorResult
from braintree.exceptions.not_found_error import NotFoundError
from braintree.resource import Resource
from braintree.resource_collection import ResourceCollection
from braintree.successful_result import SuccessfulResult

class PlanGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def all(self):
        response = self.config.http().get(self.config.base_merchant_path() + "/plans/")
        return [Plan(self.gateway, item) for item in ResourceCollection._extract_as_array(response, "plans")]

    def create(self, params=None):
        if params is None:
            params = {}
        Resource.verify_keys(params, Plan.create_signature())
        response = self.config.http().post(self.config.base_merchant_path() + "/plans", {"plan": params})
        if "plan" in response:
            return SuccessfulResult({"plan": Plan(self.gateway, response["plan"])})
        elif "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])

    def find(self, plan_id):
        try:
            if plan_id is None or plan_id.strip() == "":
                raise NotFoundError()
            response = self.config.http().get(self.config.base_merchant_path() + "/plans/" + plan_id)
            return Plan(self.gateway, response["plan"])
        except NotFoundError:
            raise NotFoundError("Plan with id " + repr(plan_id) + " not found")

    def update(self, plan_id, params=None):
        if params is None:
            params = {}
        Resource.verify_keys(params, Plan.update_signature())
        response = self.config.http().put(self.config.base_merchant_path() + "/plans/" + plan_id, {"plan": params})
        if "plan" in response:
            return SuccessfulResult({"plan": Plan(self.gateway, response["plan"])})
        elif "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])

