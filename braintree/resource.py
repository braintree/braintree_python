class Resource:
    def __init__(self, attributes):
        self.attributes = attributes

    def __getattr__(self, key):
        if key in self.attributes:
            return self.attributes[key]
        else:
            return None

    def __verify_keys(self, signature):
        pass
