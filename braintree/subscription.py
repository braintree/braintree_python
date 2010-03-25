from decimal import Decimal
from braintree.util.http import Http
from braintree.exceptions.not_found_error import NotFoundError
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.transaction import Transaction
from braintree.resource import Resource

class Subscription(Resource):
    class TrialDurationUnit(object):
        Day = "day"
        Month = "month"

    class Status(object):
        Active = "Active"
        Canceled = "Canceled"
        PastDue = "Past Due"

    @staticmethod
    def create(params={}):
        Resource.verify_keys(params, Subscription.create_signature())
        response = Http().post("/subscriptions", {"subscription": params})
        if "subscription" in response:
            return SuccessfulResult({"subscription": Subscription(response["subscription"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    @staticmethod
    def create_signature():
        return [
            "id",
            "merchant_account_id",
            "payment_method_token",
            "plan_id",
            "price",
            "trial_duration",
            "trial_duration_unit",
            "trial_period"
        ]

    @staticmethod
    def find(subscription_id):
        try:
            response = Http().get("/subscriptions/" + subscription_id)
            return Subscription(response["subscription"])
        except NotFoundError:
            raise NotFoundError("subscription with id " + subscription_id + " not found")

    @staticmethod
    def update(subscription_id, params={}):
        Resource.verify_keys(params, Subscription.update_signature())
        response = Http().put("/subscriptions/" + subscription_id, {"subscription": params})
        if "subscription" in response:
            return SuccessfulResult({"subscription": Subscription(response["subscription"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    @staticmethod
    def cancel(subscription_id):
        response = Http().put("/subscriptions/" + subscription_id + "/cancel")
        if "subscription" in response:
            return SuccessfulResult({"subscription": Subscription(response["subscription"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    @staticmethod
    def update_signature():
        return [
            "id",
            "merchant_account_id",
            "plan_id",
            "price"
        ]

    def __init__(self, attributes):
        Resource.__init__(self, attributes)
        self.price = Decimal(self.price)
        if "transactions" in attributes:
            self.transactions = [Transaction(transaction) for transaction in self.transactions]
