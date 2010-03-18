import unittest
import tests.test_helper
from nose.tools import raises
import re
import random
from datetime import datetime
from decimal import Decimal
from braintree.customer import Customer
from braintree.subscription import Subscription
from braintree.exceptions.not_found_error import NotFoundError

class TestSubscription(unittest.TestCase):
    def setUp(self):
        self.credit_card = Customer.create({
            "first_name": "Mike",
            "last_name": "Jones",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "cvv": "100"
            }
        }).customer.credit_cards[0]

        self.trial_plan = {
            "description": "Plan for integration tests -- with trial",
            "id": "integration_trial_plan",
            "price": Decimal("43.21"),
            "trial_period": True,
            "trial_duration": 2,
            "trial_duration_unit": Subscription.TrialDurationUnit.DAY
        }

        self.trialless_plan = {
            "description": "Plan for integration tests -- without a trial",
            "id": "integration_trialless_plan",
            "price": Decimal("12.34"),
            "trial_period": False
        }

    def test_create_returns_successful_result_if_valid(self):
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trialless_plan["id"]
        })

        self.assertTrue(result.is_success)
        subscription = result.subscription
        self.assertNotEquals(None, re.search("\A\w{6}\Z", subscription.id))
        self.assertEquals(Subscription.Status.ACTIVE, subscription.status)
        self.assertEquals("integration_trialless_plan", subscription.plan_id)

        self.assertEquals(datetime, type(subscription.first_billing_date))
        self.assertEquals(datetime, type(subscription.next_billing_date))
        self.assertEquals(datetime, type(subscription.billing_period_start_date))
        self.assertEquals(datetime, type(subscription.billing_period_end_date))

        self.assertEquals(0, subscription.failure_count)
        self.assertEquals(self.credit_card.token, subscription.payment_method_token)

    def test_create_can_set_the_id(self):
        new_id = str(random.randint(1, 1000000))
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trialless_plan["id"],
            "id": new_id
        })

        self.assertTrue(result.is_success)
        self.assertEquals(new_id, result.subscription.id)

    def test_create_defaults_to_plan_without_trial(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trialless_plan["id"],
        }).subscription

        self.assertEquals(self.trialless_plan["trial_period"], subscription.trial_period)
        self.assertEquals(None, subscription.trial_duration)
        self.assertEquals(None, subscription.trial_duration_unit)

    def test_create_defaults_to_plan_with_trial(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trial_plan["id"],
        }).subscription

        self.assertEquals(self.trial_plan["trial_period"], subscription.trial_period)
        self.assertEquals(self.trial_plan["trial_duration"], subscription.trial_duration)
        self.assertEquals(self.trial_plan["trial_duration_unit"], subscription.trial_duration_unit)

    def test_create_and_override_plan_with_trial(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trial_plan["id"],
            "trial_duration": 5,
            "trial_duration_unit": Subscription.TrialDurationUnit.MONTH
        }).subscription

        self.assertEquals(True, subscription.trial_period)
        self.assertEquals(5, subscription.trial_duration)
        self.assertEquals(Subscription.TrialDurationUnit.MONTH, subscription.trial_duration_unit)
