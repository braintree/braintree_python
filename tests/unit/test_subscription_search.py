from tests.test_helper import *

class TestSubscriptionSearch(unittest.TestCase):
    def test_billing_cycles_remaining_is_a_range_node(self):
        self.assertEquals(Search.RangeNodeBuilder, type(SubscriptionSearch.billing_cycles_remaining))

    def test_days_past_due_is_a_range_node(self):
        self.assertEquals(Search.RangeNodeBuilder, type(SubscriptionSearch.days_past_due))

    def test_id_is_a_text_node(self):
        self.assertEquals(Search.TextNodeBuilder, type(SubscriptionSearch.id))

    def test_merchant_account_id_is_a_multiple_value_node(self):
        self.assertEquals(Search.MultipleValueNodeBuilder, type(SubscriptionSearch.merchant_account_id))

    def test_plan_id_is_a_multiple_value_or_text_node(self):
        self.assertEquals(Search.MultipleValueOrTextNodeBuilder, type(SubscriptionSearch.plan_id))

    def test_price_is_a_range_node(self):
        self.assertEquals(Search.RangeNodeBuilder, type(SubscriptionSearch.price))

    def test_status_is_a_multiple_value_node(self):
        self.assertEquals(Search.MultipleValueNodeBuilder, type(SubscriptionSearch.status))

    def test_in_trial_period_is_multiple_value_node(self):
        self.assertEquals(Search.MultipleValueNodeBuilder, type(SubscriptionSearch.in_trial_period))

    def test_status_whitelist(self):
        SubscriptionSearch.status.in_list(
            Subscription.Status.Active,
            Subscription.Status.Canceled,
            Subscription.Status.Expired,
            Subscription.Status.PastDue
        )

    @raises(AttributeError)
    def test_status_not_in_whitelist(self):
        SubscriptionSearch.status.in_list(
            Subscription.Status.Active,
            Subscription.Status.Canceled,
            Subscription.Status.Expired,
            "not a status"
        )

    def test_ids_is_a_multiple_value_node(self):
        self.assertEquals(Search.MultipleValueNodeBuilder, type(SubscriptionSearch.ids))
