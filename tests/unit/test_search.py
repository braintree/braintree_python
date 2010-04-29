from tests.test_helper import *

class TestSearch(unittest.TestCase):
    def test_days_past_due_is(self):
        expected = {"is": "value"}
        self.assertEquals("days_past_due", SubscriptionSearch.days_past_due.name)
        self.assertEquals(expected, (SubscriptionSearch.days_past_due == "value").to_param())
        self.assertEquals(expected, (SubscriptionSearch.days_past_due.is_equal("value")).to_param())

    def test_days_past_due_is_not(self):
        expected = {"is_not": "value"}
        self.assertEquals("days_past_due", SubscriptionSearch.days_past_due.name)
        self.assertEquals(expected, (SubscriptionSearch.days_past_due != "value").to_param())
        self.assertEquals(expected, (SubscriptionSearch.days_past_due.is_not_equal("value")).to_param())

    def test_days_past_due_starts_with(self):
        expected = {"starts_with": "value"}
        self.assertEquals("days_past_due", SubscriptionSearch.days_past_due.name)
        self.assertEquals(expected, SubscriptionSearch.days_past_due.starts_with("value").to_param())

    def test_days_past_due_ends_with(self):
        expected = {"ends_with": "value"}
        self.assertEquals("days_past_due", SubscriptionSearch.days_past_due.name)
        self.assertEquals(expected, SubscriptionSearch.days_past_due.ends_with("value").to_param())

    def test_days_past_due_contains(self):
        expected = {"contains": "value"}
        self.assertEquals("days_past_due", SubscriptionSearch.days_past_due.name)
        self.assertEquals(expected, SubscriptionSearch.days_past_due.contains("value").to_param())

    def test_in_list_with_active(self):
        expected = ["active"]
        self.assertEquals("status", SubscriptionSearch.status.name)
        self.assertEquals(expected, SubscriptionSearch.status.in_list(["active"]).to_param())

    def test_in_list_with_canceled(self):
        expected = ["canceled"]
        self.assertEquals("status", SubscriptionSearch.status.name)
        self.assertEquals(expected, SubscriptionSearch.status.in_list(["canceled"]).to_param())

    def test_in_list_with_multiple_statuses(self):
        expected = ["past_due", "canceled"]
        self.assertEquals("status", SubscriptionSearch.status.name)
        self.assertEquals(expected, SubscriptionSearch.status.in_list(["past_due", "canceled"]).to_param())

    def test_key_value_node_builder_equals(self):
        builder = Search.KeyValueNodeBuilder("refund")
        node = (builder == True)

        self.assertEquals(True, node.to_param())
        self.assertEquals("refund", node.name)

    def test_key_value_node_builder_not_equals(self):
        builder = Search.KeyValueNodeBuilder("refund")
        node = (builder != True)

        self.assertEquals(False, node.to_param())
        self.assertEquals("refund", node.name)
