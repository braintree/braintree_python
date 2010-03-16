from braintree.validation_error_collection import ValidationErrorCollection

class Errors:
    def __init__(self, data):
        data["errors"] = []
        self.errors = ValidationErrorCollection(data)
        self.size = self.errors.deep_size

    def for_object(self, key):
        return self.errors.for_object(key)
