from tests.test_helper import *

class TestSearch(unittest.TestCase):
    def test_text_node_is(self):
        node = Search.TextNodeBuilder("name")
        self.assertEquals({"is": "value"}, (node == "value").to_param())

    def test_text_node_is_not(self):
        node = Search.TextNodeBuilder("name")
        self.assertEquals({"is_not": "value"}, (node != "value").to_param())

    def test_text_node_starts_with(self):
        node = Search.TextNodeBuilder("name")
        self.assertEquals({"starts_with": "value"}, (node.starts_with("value")).to_param())

    def test_text_node_ends_with(self):
        node = Search.TextNodeBuilder("name")
        self.assertEquals({"ends_with": "value"}, (node.ends_with("value")).to_param())

    def test_text_node_contains(self):
        node = Search.TextNodeBuilder("name")
        self.assertEquals({"contains": "value"}, (node.contains("value")).to_param())

    def test_multiple_value_node_in_list(self):
        node = Search.MultipleValueNodeBuilder("name")
        self.assertEquals(["value1", "value2"], (node.in_list(["value1", "value2"])).to_param())

    def test_multiple_value_node_in_list_as_arg_list(self):
        node = Search.MultipleValueNodeBuilder("name")
        self.assertEquals(["value1", "value2"], (node.in_list("value1", "value2")).to_param())

    def test_multiple_value_node_is(self):
        node = Search.MultipleValueNodeBuilder("name")
        self.assertEquals(["value1"], (node == "value1").to_param())

    def test_range_node_min_ge(self):
        node = Search.RangeNodeBuilder("name")
        self.assertEquals({"min": "value"}, (node >= "value").to_param())

    def test_range_node_min_greater_than_or_equal_to(self):
        node = Search.RangeNodeBuilder("name")
        self.assertEquals({"min": "value"}, (node.greater_than_or_equal_to("value")).to_param())

    def test_range_node_max_le(self):
        node = Search.RangeNodeBuilder("name")
        self.assertEquals({"max": "value"}, (node <= "value").to_param())

    def test_range_node_max_less_than_or_equal_to(self):
        node = Search.RangeNodeBuilder("name")
        self.assertEquals({"max": "value"}, (node.less_than_or_equal_to("value")).to_param())

    def test_range_node_between(self):
        node = Search.RangeNodeBuilder("name")
        self.assertEquals({"min": "min_value", "max": "max_value"}, (node.between("min_value", "max_value")).to_param())


