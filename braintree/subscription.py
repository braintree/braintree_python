from decimal import Decimal
from braintree.util.http import Http
from braintree.exceptions.not_found_error import NotFoundError
from braintree.resource_collection import ResourceCollection
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.transaction import Transaction
from braintree.resource import Resource

class Subscription(Resource):
    """
    A class representing a Subscription.

    An example of creating a subscription with all available fields::

        result = braintree.Subscription.create({
            "id": "my_subscription_id",
            "merchant_account_id": "merchant_account_one",
            "payment_method_token": "my_payment_token",
            "plan_id": "some_plan_id",
            "price": "29.95",
            "trial_duration": 1,
            "trial_duration_unit": braintree.Subscription.TrialDurationUnit.Month,
            "trial_period": True
        })

    For more information on Subscriptions, see http://www.braintreepaymentsolutions.com/gateway/subscription-api
    """

    class TrialDurationUnit(object):
        """
        Constants representing trial duration units.  Available types are:

        * braintree.Subscription.TrialDurationUnit.Day
        * braintree.Subscription.TrialDurationUnit.Month
        """

        Day = "day"
        Month = "month"

    class Status(object):
        """
        Constants representing subscription statusues.  Available statuses are:

        * braintree.Subscription.Status.Active
        * braintree.Subscription.Status.Canceled
        * braintree.Subscription.Status.PastDue
        """

        Active = "Active"
        Canceled = "Canceled"
        PastDue = "Past Due"

    @staticmethod
    def create(params={}):
        """
        Create a Subscription:::

            result = braintree.Subscription.create({
                "payment_method_token": "my_payment_token",
                "plan_id": "some_plan_id",
            })
        """
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
        """
        Find a subscription given a subscription_id.  This does not return a result
        object.  This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>`
        if the provided subscription_id is not found. ::

            subscription = braintree.Subscription.find("my_subscription_id")
        """

        try:
            response = Http().get("/subscriptions/" + subscription_id)
            return Subscription(response["subscription"])
        except NotFoundError:
            raise NotFoundError("subscription with id " + subscription_id + " not found")

    @staticmethod
    def update(subscription_id, params={}):
        """
        Update an existing subscription by subscription_id.  The params are similar to create::


            result = braintree.Subscription.update("my_subscription_id", {
                "price": "9.99",
            })
        """

        Resource.verify_keys(params, Subscription.update_signature())
        response = Http().put("/subscriptions/" + subscription_id, {"subscription": params})
        if "subscription" in response:
            return SuccessfulResult({"subscription": Subscription(response["subscription"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    @staticmethod
    def cancel(subscription_id):
        """
        Cancel a subscription by subscription_id:::

            result = braintree.Subscription.cancel("my_subscription_id")
        """
        response = Http().put("/subscriptions/" + subscription_id + "/cancel")
        if "subscription" in response:
            return SuccessfulResult({"subscription": Subscription(response["subscription"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    @staticmethod
    def search(search_terms, page=1):
        """
        Allows searching on subscriptions. There are two types of fields that are searchable: text and
        multiple value fields. Searchable text fields are:
        - plan_id
        - days_past_due

        Searchable multiple value fields are:
        - status

        For text fields, you can search using the following operators: ==, !=, starts_with, ends_with
        and contains. For mutiple value fields, you can search using the in_list operator. An example::

            braintree.Subscription.search([
                braintree.SubscriptionSearch.plan_id.starts_with("abc"),
                braintree.SubscriptionSearch.days_past_due == "30",
                braintree.SubscriptionSearch.status.in_list([braintree.Subscription.Status.PastDue])
            ])
        """
        criteria = {}
        for term in search_terms:
            if criteria.get(term.name):
                criteria[term.name] = dict(criteria[term.name].items() + term.to_param().items())
            else:
                criteria[term.name] = term.to_param()

        response = Http().post("/subscriptions/advanced_search?page=" + str(page), {"search": criteria})
        return ResourceCollection(search_terms, response["subscriptions"], Subscription)

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
