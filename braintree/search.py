class Search:
    class KeyValueNodeBuilder(object):
        def __init__(self, name):
            self.name = name

        def __eq__(self, value):
            return self.is_equal(value)

        def is_equal(self, value):
            return Search.TextNode(self.name, value)

        def __ne__(self, value):
            return self.is_not_equal(value)

        def is_not_equal(self, value):
            return Search.TextNode(self.name, not value)

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

        def __eq__(self, value):
            return self.in_list([value])

    class MultipleValueNode(object):
        def __init__(self, name, items):
            self.name = name
            self.items = items

        def to_param(self):
            return self.items

    class RangeNodeBuilder(object):
        def __init__(self, name):
            self.name = name

        def __ge__(self, min):
            return self.greater_than_or_equal_to(min)

        def greater_than_or_equal_to(self, min):
            return Search.TextNode(self.name, {"min": min})

        def __le__(self, max):
            return self.less_than_or_equal_to(max)

        def less_than_or_equal_to(self, max):
            return Search.TextNode(self.name, {"max": max})

        def between(self, min, max):
            return Search.TextNode(self.name, {"min": min, "max": max})
