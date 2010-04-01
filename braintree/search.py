class Search:
    class TextNode:
        def __init__(self, name):
            self.name = name
            self.dict = {}

        def __eq__(self, value):
            self.dict["is"] = value
            return self

        def __ne__(self, value):
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
            dict = self.dict
            self.dict = {}
            return dict

    @staticmethod
    def text_nodes(*names):
        for name in names:
            Search.__dict__[name] = Search.TextNode(name)

Search.text_nodes(
    "plan_id",
    "days_past_due"
)
