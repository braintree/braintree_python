from braintree.errors import Errors

class ErrorResult(object):
    def __init__(self, attributes):
        self.is_success = False
        self.params = attributes["params"]
        self.errors = Errors(attributes["errors"])

