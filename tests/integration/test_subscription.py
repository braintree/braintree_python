from tests.test_helper import *

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
            "trial_duration_unit": Subscription.TrialDurationUnit.Day
        }

        self.trialless_plan = {
            "description": "Plan for integration tests -- without a trial",
            "id": "integration_trialless_plan",
            "price": Decimal("12.34"),
            "trial_period": False
        }

        self.updateable_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "price": Decimal("54.32"),
            "plan_id": self.trialless_plan["id"]
        }).subscription

        self.default_merchant_account_id = "sandbox_credit_card"
        self.non_default_merchant_account_id = "sandbox_credit_card_non_default"

    def test_create_returns_successful_result_if_valid(self):
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trialless_plan["id"]
        })

        self.assertTrue(result.is_success)
        subscription = result.subscription
        self.assertNotEquals(None, re.search("\A\w{6}\Z", subscription.id))
        self.assertEquals(Subscription.Status.Active, subscription.status)
        self.assertEquals("integration_trialless_plan", subscription.plan_id)
        self.assertEquals(self.default_merchant_account_id, subscription.merchant_account_id)

        self.assertEquals(date, type(subscription.first_billing_date))
        self.assertEquals(date, type(subscription.next_billing_date))
        self.assertEquals(date, type(subscription.billing_period_start_date))
        self.assertEquals(date, type(subscription.billing_period_end_date))

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

    def test_create_can_set_the_merchant_account_id(self):
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trialless_plan["id"],
            "merchant_account_id": self.non_default_merchant_account_id
        })

        self.assertTrue(result.is_success)
        self.assertEquals(self.non_default_merchant_account_id, result.subscription.merchant_account_id)

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
            "trial_duration_unit": Subscription.TrialDurationUnit.Month
        }).subscription

        self.assertEquals(True, subscription.trial_period)
        self.assertEquals(5, subscription.trial_duration)
        self.assertEquals(Subscription.TrialDurationUnit.Month, subscription.trial_duration_unit)

    def test_create_and_override_trial_period(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trial_plan["id"],
            "trial_period": False
        }).subscription

        self.assertEquals(False, subscription.trial_period)

    def test_create_creates_a_transaction_if_no_trial_period(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trialless_plan["id"],
        }).subscription

        self.assertEquals(1, len(subscription.transactions))
        transaction = subscription.transactions[0]
        self.assertEquals(Transaction, type(transaction))
        self.assertEquals(self.trialless_plan["price"], transaction.amount)
        self.assertEquals("sale", transaction.type)

    def test_create_doesnt_creates_a_transaction_if_trial_period(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trial_plan["id"],
        }).subscription

        self.assertEquals(0, len(subscription.transactions))

    def test_create_with_error_result(self):
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trial_plan["id"],
            "id": "invalid token"
        })

        self.assertFalse(result.is_success)
        self.assertEquals("81906", result.errors.for_object("subscription").on("id")[0].code)

    def test_find_with_valid_id(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trial_plan["id"],
        }).subscription

        found_subscription = Subscription.find(subscription.id)
        self.assertEquals(subscription.id, found_subscription.id)

    def test_find_with_invalid_token(self):
        try:
            Subscription.find("bad_token")
            self.assertTrue(False)
        except Exception, e:
            self.assertEquals("subscription with id bad_token not found", str(e))

    def test_update_with_successful_result(self):
        new_id = str(random.randint(1, 1000000))
        result = Subscription.update(self.updateable_subscription.id, {
            "id": new_id,
            "price": Decimal("9999.88"),
            "plan_id": self.trial_plan["id"]
        })

        self.assertTrue(result.is_success)

        subscription = result.subscription
        self.assertEquals(new_id, subscription.id)
        self.assertEquals(self.trial_plan["id"], subscription.plan_id)
        self.assertEquals(Decimal("9999.88"), subscription.price)

    def test_update_with_merchant_account_id(self):
        result = Subscription.update(self.updateable_subscription.id, {
            "merchant_account_id": self.non_default_merchant_account_id,
        })

        self.assertTrue(result.is_success)

        subscription = result.subscription
        self.assertEquals(self.non_default_merchant_account_id, subscription.merchant_account_id)

    def test_update_with_error_result(self):
        result = Subscription.update(self.updateable_subscription.id, {
            "id": "bad id",
        })

        self.assertFalse(result.is_success)
        self.assertEquals("81906", result.errors.for_object("subscription").on("id")[0].code)

    @raises(NotFoundError)
    def test_update_raises_error_when_subscription_not_found(self):
        Subscription.update("notfound", {
            "id": "newid",
        })

    def test_cancel_with_successful_response(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trialless_plan["id"]
        }).subscription

        result = Subscription.cancel(subscription.id)
        self.assertTrue(result.is_success)
        self.assertEqual("Canceled", result.subscription.status)

    def test_unsuccessful_cancel_returns_validation_error(self):
        Subscription.cancel(self.updateable_subscription.id)
        result = Subscription.cancel(self.updateable_subscription.id)

        self.assertFalse(result.is_success)
        self.assertEquals("81905", result.errors.for_object("subscription").on("status")[0].code)

    @raises(NotFoundError)
    def test_cancel_raises_not_found_error_with_bad_subscription(self):
        Subscription.cancel("notreal")

    def test_search_on_plan_id_is(self):
        trial_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trial_plan["id"]
        }).subscription

        trialless_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trialless_plan["id"]
        }).subscription

        collection = Subscription.search([
            Search.plan_id == "integration_trial_plan"
        ])

        self.assertTrue(TestHelper.includes_on_any_page(collection, trial_subscription))
        self.assertFalse(TestHelper.includes_on_any_page(collection, trialless_subscription))

    def test_search_on_plan_id_starts_with(self):
        trial_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trial_plan["id"]
        }).subscription

        trialless_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trialless_plan["id"]
        }).subscription

        collection = Subscription.search([
            Search.plan_id.starts_with("integration_trial_p")
        ])

        self.assertTrue(TestHelper.includes_on_any_page(collection, trial_subscription))
        self.assertFalse(TestHelper.includes_on_any_page(collection, trialless_subscription))

    def test_search_on_plan_id_ends_with(self):
        trial_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trial_plan["id"]
        }).subscription

        trialless_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trialless_plan["id"]
        }).subscription

        collection = Subscription.search([
            Search.plan_id.ends_with("trial_plan")
        ])

        self.assertTrue(TestHelper.includes_on_any_page(collection, trial_subscription))
        self.assertFalse(TestHelper.includes_on_any_page(collection, trialless_subscription))

    def test_search_on_plan_id_is_not(self):
        trial_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trial_plan["id"]
        }).subscription

        trialless_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trialless_plan["id"]
        }).subscription

        collection = Subscription.search([
            Search.plan_id != "integration_trialless_plan"
        ])

        self.assertTrue(TestHelper.includes_on_any_page(collection, trial_subscription))
        self.assertFalse(TestHelper.includes_on_any_page(collection, trialless_subscription))

    def test_search_on_plan_id_contains(self):
        trial_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trial_plan["id"]
        }).subscription

        trialless_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trialless_plan["id"]
        }).subscription

        collection = Subscription.search([
            Search.plan_id.contains("rial_pl")
        ])

        self.assertTrue(TestHelper.includes_on_any_page(collection, trial_subscription))
        self.assertFalse(TestHelper.includes_on_any_page(collection, trialless_subscription))

    def test_search_on_status(self):
        active_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trialless_plan["id"]
        }).subscription

        canceled_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trialless_plan["id"]
        }).subscription
        Subscription.cancel(canceled_subscription.id)

        collection = Subscription.search([
            Search.status.in_list([Subscription.Status.Active])
        ])

        self.assertTrue(TestHelper.includes_on_any_page(collection, active_subscription))
        self.assertFalse(TestHelper.includes_on_any_page(collection, canceled_subscription))

    def test_search_on_multiple_values(self):
        active_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trialless_plan["id"]
        }).subscription

        canceled_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": self.trialless_plan["id"]
        }).subscription
        Subscription.cancel(canceled_subscription.id)

        collection = Subscription.search([
            Search.plan_id == "integration_trialless_plan",
            Search.status.in_list([Subscription.Status.Active]),
        ])

        self.assertTrue(TestHelper.includes_on_any_page(collection, active_subscription))
        self.assertFalse(TestHelper.includes_on_any_page(collection, canceled_subscription))

