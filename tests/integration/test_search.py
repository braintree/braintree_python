from tests.test_helper import *

class TestSearch(unittest.TestCase):
    def test_text_node_is(self):
        credit_card = Customer.create({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
            }
        }).customer.credit_cards[0]

        trial_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trial_plan["id"]
        }).subscription

        trialless_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription

        collection = Subscription.search([
            SubscriptionSearch.plan_id == "integration_trial_plan"
        ])

        self.assertTrue(TestHelper.includes(collection, trial_subscription))
        self.assertFalse(TestHelper.includes(collection, trialless_subscription))

    def test_text_node_is_not(self):
        credit_card = Customer.create({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
            }
        }).customer.credit_cards[0]

        trial_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trial_plan["id"]
        }).subscription

        trialless_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription

        collection = Subscription.search([
            SubscriptionSearch.plan_id != "integration_trialless_plan"
        ])

        self.assertTrue(TestHelper.includes(collection, trial_subscription))
        self.assertFalse(TestHelper.includes(collection, trialless_subscription))

    def test_text_node_starts_with(self):
        credit_card = Customer.create({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
            }
        }).customer.credit_cards[0]

        trial_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trial_plan["id"]
        }).subscription

        trialless_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription

        collection = Subscription.search([
            SubscriptionSearch.plan_id.starts_with("integration_trial_p")
        ])

        self.assertTrue(TestHelper.includes(collection, trial_subscription))
        self.assertFalse(TestHelper.includes(collection, trialless_subscription))

    def test_text_node_ends_with(self):
        credit_card = Customer.create({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
            }

        }).customer.credit_cards[0]
        trial_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trial_plan["id"]
        }).subscription

        trialless_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription

        collection = Subscription.search([
            SubscriptionSearch.plan_id.ends_with("trial_plan")
        ])

        self.assertTrue(TestHelper.includes(collection, trial_subscription))
        self.assertFalse(TestHelper.includes(collection, trialless_subscription))

    def test_text_node_contains(self):
        credit_card = Customer.create({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
            }
        }).customer.credit_cards[0]

        trial_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trial_plan["id"]
        }).subscription

        trialless_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription

        collection = Subscription.search([
            SubscriptionSearch.plan_id.contains("rial_pl")
        ])

        self.assertTrue(TestHelper.includes(collection, trial_subscription))
        self.assertFalse(TestHelper.includes(collection, trialless_subscription))

    def test_multiple_value_node_in_list(self):
        credit_card = Customer.create({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
            }
        }).customer.credit_cards[0]

        active_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription

        canceled_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription
        Subscription.cancel(canceled_subscription.id)

        collection = Subscription.search([
            SubscriptionSearch.status.in_list([Subscription.Status.Active, Subscription.Status.Canceled])
        ])

        self.assertTrue(TestHelper.includes(collection, active_subscription))
        self.assertTrue(TestHelper.includes(collection, canceled_subscription))

    def test_multiple_value_node_in_list_as_arg_list(self):
        credit_card = Customer.create({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
            }
        }).customer.credit_cards[0]

        active_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription

        canceled_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription
        Subscription.cancel(canceled_subscription.id)

        collection = Subscription.search([
            SubscriptionSearch.status.in_list(Subscription.Status.Active, Subscription.Status.Canceled)
        ])

        self.assertTrue(TestHelper.includes(collection, active_subscription))
        self.assertTrue(TestHelper.includes(collection, canceled_subscription))

    def test_multiple_value_node_is(self):
        credit_card = Customer.create({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
            }
        }).customer.credit_cards[0]

        active_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription

        canceled_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription
        Subscription.cancel(canceled_subscription.id)

        collection = Subscription.search([
            SubscriptionSearch.status == Subscription.Status.Active
        ])

        self.assertTrue(TestHelper.includes(collection, active_subscription))
        self.assertFalse(TestHelper.includes(collection, canceled_subscription))

    def test_range_node_min(self):
        name = "Henrietta Livingston%s" % randint(1,100000)
        t_1500 = Transaction.sale({
            "amount": "1500.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": name
            }
        }).transaction

        t_1800 = Transaction.sale({
            "amount": "1800.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": name
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.credit_card_cardholder_name == name,
            TransactionSearch.amount >= "1700"
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(t_1800.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.credit_card_cardholder_name == name,
            TransactionSearch.amount.greater_than_or_equal_to("1700")
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(t_1800.id, collection.first.id)

    def test_range_node_max(self):
        name = "Henrietta Livingston%s" % randint(1,100000)
        t_1500 = Transaction.sale({
            "amount": "1500.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": name
            }
        }).transaction

        t_1800 = Transaction.sale({
            "amount": "1800.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": name
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.credit_card_cardholder_name == name,
            TransactionSearch.amount <= "1700"
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(t_1500.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.credit_card_cardholder_name == name,
            TransactionSearch.amount.less_than_or_equal_to("1700")
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(t_1500.id, collection.first.id)

    def test_range_node_is(self):
        name = "Henrietta Livingston%s" % randint(1,100000)
        t_1500 = Transaction.sale({
            "amount": "1500.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": name
            }
        }).transaction

        t_1800 = Transaction.sale({
            "amount": "1800.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": name
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.credit_card_cardholder_name == name,
            TransactionSearch.amount == "1800"
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(t_1800.id, collection.first.id)

    def test_range_node_between(self):
        name = "Henrietta Livingston%s" % randint(1,100000)
        t_1000 = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": name
            }
        }).transaction

        t_1500 = Transaction.sale({
            "amount": "1500.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": name
            }
        }).transaction

        t_1800 = Transaction.sale({
            "amount": "1800.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": name
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.credit_card_cardholder_name == name,
            TransactionSearch.amount.between("1100", "1600")
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(t_1500.id, collection.first.id)

    def test_search_on_multiple_values(self):
        credit_card = Customer.create({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
            }
        }).customer.credit_cards[0]

        active_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription

        canceled_subscription = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription
        Subscription.cancel(canceled_subscription.id)

        collection = Subscription.search([
            SubscriptionSearch.plan_id == "integration_trialless_plan",
            SubscriptionSearch.status.in_list([Subscription.Status.Active])
        ])

        self.assertTrue(TestHelper.includes(collection, active_subscription))
        self.assertFalse(TestHelper.includes(collection, canceled_subscription))

