class Search:
    class TextNodeBuilder(object):
        def __init__(self, name):
            self.name = name

        def __eq__(self, value):
            return self.is_equal(value)

        def is_equal(self, value):
            return Search.TextNode(self.name, {"is": value})

        def __ne__(self, value):
            return self.is_not_equal(value)

        def is_not_equal(self, value):
            return Search.TextNode(self.name, {"is_not": value})

        def starts_with(self, value):
            return Search.TextNode(self.name, {"starts_with": value})

        def ends_with(self, value):
            return Search.TextNode(self.name, {"ends_with": value})

        def contains(self, value):
            return Search.TextNode(self.name, {"contains": value})

    class TextNode(object):
        def __init__(self, name, dict):
          self.name = name
          self.dict = dict

        def to_param(self):
            return self.dict

    class MultipleValueNodeBuilder(object):
        def __init__(self, name):
            self.name = name

        def in_list(self, list):
            return Search.MultipleValueNode(self.name, list)

    class MultipleValueNode(object):
        def __init__(self, name, items):
            self.name = name
            self.items = items

        def to_param(self):
            return self.items

