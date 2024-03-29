from tests.test_helper import *

class TestSearch(unittest.TestCase):
    def test_text_node_is(self):
        node = Search.TextNodeBuilder("name")
        self.assertEqual({"is": "value"}, (node == "value").to_param())

    def test_text_node_is_not(self):
        node = Search.TextNodeBuilder("name")
        self.assertEqual({"is_not": "value"}, (node != "value").to_param())

    def test_text_node_starts_with(self):
        node = Search.TextNodeBuilder("name")
        self.assertEqual({"starts_with": "value"}, (node.starts_with("value")).to_param())

    def test_text_node_ends_with(self):
        node = Search.TextNodeBuilder("name")
        self.assertEqual({"ends_with": "value"}, (node.ends_with("value")).to_param())

    def test_text_node_contains(self):
        node = Search.TextNodeBuilder("name")
        self.assertEqual({"contains": "value"}, (node.contains("value")).to_param())

    def test_multiple_value_node_in_list(self):
        node = Search.MultipleValueNodeBuilder("name")
        self.assertEqual(["value1", "value2"], (node.in_list(["value1", "value2"])).to_param())

    def test_multiple_value_node_in_list_as_arg_list(self):
        node = Search.MultipleValueNodeBuilder("name")
        self.assertEqual(["value1", "value2"], (node.in_list("value1", "value2")).to_param())

    def test_multiple_value_node_is(self):
        node = Search.MultipleValueNodeBuilder("name")
        self.assertEqual(["value1"], (node == "value1").to_param())

    def test_multiple_value_node_with_value_in_whitelist(self):
        node = Search.MultipleValueNodeBuilder("name", ["okay"])
        self.assertEqual(["okay"], (node == "okay").to_param())

    def test_multiple_value_node_with_value_not_in_whitelist(self):
        with self.assertRaises(AttributeError):
            node = Search.MultipleValueNodeBuilder("name", ["okay", "also okay"])
            node == "not okay"

    def test_multiple_value_or_text_node_is(self):
        node = Search.MultipleValueOrTextNodeBuilder("name")
        self.assertEqual({"is": "value"}, (node == "value").to_param())

    def test_multiple_value_or_text_node_is_not(self):
        node = Search.MultipleValueOrTextNodeBuilder("name")
        self.assertEqual({"is_not": "value"}, (node != "value").to_param())

    def test_multiple_value_or_text_node_starts_with(self):
        node = Search.MultipleValueOrTextNodeBuilder("name")
        self.assertEqual({"starts_with": "value"}, (node.starts_with("value")).to_param())

    def test_multiple_value_or_text_node_ends_with(self):
        node = Search.MultipleValueOrTextNodeBuilder("name")
        self.assertEqual({"ends_with": "value"}, (node.ends_with("value")).to_param())

    def test_multiple_value_or_text_node_contains(self):
        node = Search.MultipleValueOrTextNodeBuilder("name")
        self.assertEqual({"contains": "value"}, (node.contains("value")).to_param())

    def test_multiple_value_or_text_node_in_list(self):
        node = Search.MultipleValueOrTextNodeBuilder("name")
        self.assertEqual(["value1", "value2"], (node.in_list(["value1", "value2"])).to_param())

    def test_multiple_value_or_text_node_in_list_as_arg_list(self):
        node = Search.MultipleValueOrTextNodeBuilder("name")
        self.assertEqual(["value1", "value2"], (node.in_list("value1", "value2")).to_param())

    def test_multiple_value_or_text_node_with_value_in_whitelist(self):
        node = Search.MultipleValueOrTextNodeBuilder("name", ["okay"])
        self.assertEqual(["okay"], node.in_list("okay").to_param())

    def test_multiple_value_or_text_node_with_value_not_in_whitelist(self):
        with self.assertRaises(AttributeError):
            node = Search.MultipleValueOrTextNodeBuilder("name", ["okay"])
            node.in_list("not okay").to_param()

    def test_range_node_min_ge(self):
        node = Search.RangeNodeBuilder("name")
        self.assertEqual({"min": "value"}, (node >= "value").to_param())

    def test_range_node_min_greater_than_or_equal_to(self):
        node = Search.RangeNodeBuilder("name")
        self.assertEqual({"min": "value"}, (node.greater_than_or_equal_to("value")).to_param())

    def test_range_node_max_le(self):
        node = Search.RangeNodeBuilder("name")
        self.assertEqual({"max": "value"}, (node <= "value").to_param())

    def test_range_node_max_less_than_or_equal_to(self):
        node = Search.RangeNodeBuilder("name")
        self.assertEqual({"max": "value"}, (node.less_than_or_equal_to("value")).to_param())

    def test_range_node_between(self):
        node = Search.RangeNodeBuilder("name")
        self.assertEqual({"min": "min_value", "max": "max_value"}, (node.between("min_value", "max_value")).to_param())

    def test_range_node_is(self):
        node = Search.RangeNodeBuilder("name")
        self.assertEqual({"is": "value"}, (node == "value").to_param())

    def test_key_value_node_is_eq(self):
        node = Search.KeyValueNodeBuilder("name")
        self.assertTrue((node == True).to_param())

    def test_key_value_node_is_equal(self):
        node = Search.KeyValueNodeBuilder("name")
        self.assertEqual(True, (node.is_equal(True)).to_param())

    def test_key_value_node_is_not_equal(self):
        node = Search.KeyValueNodeBuilder("name")
        self.assertEqual(False, (node.is_not_equal(True)).to_param())

    def test_key_value_node_symbols_is_not_equal(self):
        node = Search.KeyValueNodeBuilder("name")
        self.assertEqual(False, (node != True).to_param())
