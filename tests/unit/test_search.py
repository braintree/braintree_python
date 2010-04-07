from tests.test_helper import *

class TestSearch(unittest.TestCase):
    def test_days_past_due_is(self):
        expected = {"is": "value"}
        self.assertEquals("days_past_due", Search().days_past_due.name)
        self.assertEquals(expected, (Search().days_past_due == "value").to_param())
        self.assertEquals(expected, (Search().days_past_due.is_equal("value")).to_param())

    def test_days_past_due_is_not(self):
        expected = {"is_not": "value"}
        self.assertEquals("days_past_due", Search().days_past_due.name)
        self.assertEquals(expected, (Search().days_past_due != "value").to_param())
        self.assertEquals(expected, (Search().days_past_due.is_not_equal("value")).to_param())

    def test_days_past_due_starts_with(self):
        expected = {"starts_with": "value"}
        self.assertEquals("days_past_due", Search().days_past_due.name)
        self.assertEquals(expected, Search().days_past_due.starts_with("value").to_param())

    def test_days_past_due_ends_with(self):
        expected = {"ends_with": "value"}
        self.assertEquals("days_past_due", Search().days_past_due.name)
        self.assertEquals(expected, Search().days_past_due.ends_with("value").to_param())

    def test_days_past_due_contains(self):
        expected = {"contains": "value"}
        self.assertEquals("days_past_due", Search().days_past_due.name)
        self.assertEquals(expected, Search().days_past_due.contains("value").to_param())
