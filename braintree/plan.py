from braintree.util.http import Http
import braintree
from braintree.add_on import AddOn
from braintree.configuration import Configuration
from braintree.discount import Discount
from braintree.resource_collection import ResourceCollection
from braintree.resource import Resource
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult

class Plan(Resource):

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        if "add_ons" in attributes:
            self.add_ons = [AddOn(gateway, add_on) for add_on in self.add_ons]
        if "discounts" in attributes:
            self.discounts = [Discount(gateway, discount) for discount in self.discounts]

    @staticmethod
    def all():
        return Configuration.gateway().plan.all()

    @staticmethod
    def create(params=None):
        if params is None:
            params = {}
        return Configuration.gateway().plan.create(params)

    @staticmethod
    def find(subscription_id):
        return Configuration.gateway().plan.find(subscription_id)

    @staticmethod
    def update(subscription_id, params=None):
        if params is None:
            params = {}
        return Configuration.gateway().plan.update(subscription_id, params)

    @staticmethod
    def create_signature():
        return [
            "billing_day_of_month",
            "billing_frequency",
            "currency_iso_code",
            "description",
            "id",
            "merchant_id",
            "name",
            "number_of_billing_cycles",
            "price",
            "trial_duration",
            "trial_duration_unit",
            "trial_period"
        ] + Plan._add_on_discount_signature()

    @staticmethod
    def update_signature():
        return [
            "billing_day_of_month",
            "billing_frequency",
            "currency_iso_code",
            "description",
            "id",
            "merchant_id",
            "name",
            "number_of_billing_cycles",
            "price",
            "trial_duration",
            "trial_duration_unit",
            "trial_period"
        ] + Plan._add_on_discount_signature()

    @staticmethod
    def _add_on_discount_signature():
        return [
            {
                "add_ons": [
                    {"add": ["amount", "inherited_from_id", "never_expires", "number_of_billing_cycles", "quantity"]},
                    {"update": ["amount", "existing_id", "never_expires", "number_of_billing_cycles", "quantity"]},
                    {"remove": ["_any_key_"]}
                ]
            },
            {
                "discounts": [
                    {"add": ["amount", "inherited_from_id", "never_expires", "number_of_billing_cycles", "quantity"]},
                    {"update": ["amount", "existing_id", "never_expires", "number_of_billing_cycles", "quantity"]},
                    {"remove": ["_any_key_"]}
                ]
            }
        ]

