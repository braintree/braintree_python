class Search:
    def __init__(self):
        self.plan_id = Search.TextNode("plan_id")
        self.days_past_due = Search.TextNode("days_past_due")
        self.status = Search.MultipleValueNode("status")

    class TextNode(object):
        def __init__(self, name):
            self.name = name
            self.dict = {}

        def __eq__(self, value):
            return self.is_equal(value)

        def is_equal(self, value):
            self.dict["is"] = value
            return self

        def __ne__(self, value):
            return self.is_not_equal(value)

        def is_not_equal(self, value):
            self.dict["is_not"] = value
            return self

        def starts_with(self, value):
            self.dict["starts_with"] = value
            return self

        def ends_with(self, value):
            self.dict["ends_with"] = value
            return self

        def contains(self, value):
            self.dict["contains"] = value
            return self

        def to_param(self):
            return self.dict

    class MultipleValueNode(object):
        def __init__(self, name):
            self.name = name
            self.items = []

        def in_list(self, list):
            self.items = list
            return self

        def to_param(self):
            return self.items
