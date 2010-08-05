from tests.test_helper import *

class TestSubscriptionSearch(unittest.TestCase):
    def test_days_past_due_is_a_text_node(self):
        self.assertEquals(Search.TextNodeBuilder, type(SubscriptionSearch.days_past_due))

    def test_plan_id_is_a_text_node(self):
        self.assertEquals(Search.TextNodeBuilder, type(SubscriptionSearch.plan_id))

    def test_status_is_a_multiple_value_node(self):
        self.assertEquals(Search.MultipleValueNodeBuilder, type(SubscriptionSearch.status))

    def test_ids_is_a_multiple_value_node(self):
        self.assertEquals(Search.MultipleValueNodeBuilder, type(SubscriptionSearch.ids))

