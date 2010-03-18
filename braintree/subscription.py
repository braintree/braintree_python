from braintree.util.http import Http
from braintree.exceptions.not_found_error import NotFoundError
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.resource import Resource

class Subscription(Resource):
    class TrialDurationUnit(object):
        DAY = "day"
        MONTH = "month"

    class Status(object):
      ACTIVE = 'Active'
      CANCELED = 'Canceled'
      PAST_DUE = 'Past Due'

    @staticmethod
    def create(params={}):
        #Resource.verify_keys(params, CreditCard.create_signature())
        response = Http().post("/subscriptions", {"subscription": params})
        #if "credit_card" in response:
        return SuccessfulResult({"subscription": Subscription(response["subscription"])})
        #elif "api_error_response" in response:
        #    return ErrorResult(response["api_error_response"])
