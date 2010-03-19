from braintree.validation_error import ValidationError

class ValidationErrorCollection(object):
    def __init__(self, data={"errors": []}):
        self.errors = [ValidationError(error) for error in data["errors"]]
        self.nested_errors = self.__nested_errors(data)
        self.deep_size = self.__deep_size()
        self.size = len(self.errors)

    def all(self):
        result = []
        result.extend(self.errors)
        for nested_error in self.nested_errors.values():
            result.extend(nested_error.all())
        return result

    def for_object(self, nested_key):
        return self.__get_nested_errrors(nested_key)

    def on(self, attribute):
        return [error for error in self.errors if error.attribute == attribute]

    def __deep_size(self):
        size = len(self.errors)
        for error in self.nested_errors.values():
            size += error.deep_size
        return size

    def __get_nested_errrors(self, nested_key):
        if nested_key in self.nested_errors:
            return self.nested_errors[nested_key]
        else:
            return ValidationErrorCollection()

    def __getitem__(self, index):
        return self.errors[index]

    def __len__(self):
        return self.size

    def __nested_errors(self, data):
        nested_errors = {}
        for key in data.keys():
            if key == "errors": continue
            nested_errors[key] = ValidationErrorCollection(data[key])
        return nested_errors
