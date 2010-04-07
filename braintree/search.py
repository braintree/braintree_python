class Search:
    class TextNode(object):
        def __init__(self, name):
            self.name = name
            self.dict = {}

        def __eq__(self, value):
            return self.is_equal(value)

        def is_equal(self, value):
            clone = self.clone()
            clone.dict["is"] = value
            return clone

        def __ne__(self, value):
            return self.is_not_equal(value)

        def is_not_equal(self, value):
            clone = self.clone()
            clone.dict["is_not"] = value
            return clone

        def starts_with(self, value):
            clone = self.clone()
            clone.dict["starts_with"] = value
            return clone

        def ends_with(self, value):
            clone = self.clone()
            clone.dict["ends_with"] = value
            return clone

        def contains(self, value):
            clone = self.clone()
            clone.dict["contains"] = value
            return clone

        def to_param(self):
            return self.dict

        def clone(self):
            return Search.TextNode(self.name)

    class MultipleValueNode(object):
        def __init__(self, name):
            self.name = name
            self.items = []

        def in_list(self, list):
            self.items = list
            return self

        def to_param(self):
            return self.items

    plan_id = TextNode("plan_id")
    days_past_due = TextNode("days_past_due")
    status = MultipleValueNode("status")

