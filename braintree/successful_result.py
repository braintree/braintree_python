class SuccessfulResult:
    def __init__(self, attributes):
        self.attributes = attributes

    def is_success(self):
        return True

    def __getattr__(self, key):
        if key in self.attributes:
            return self.attributes[key]
        else:
            return None
