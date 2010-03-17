from braintree.errors import Errors
from braintree.credit_card_verification import CreditCardVerification

class ErrorResult(object):
    def __init__(self, attributes):
        self.is_success = False
        self.params = attributes["params"]
        self.errors = Errors(attributes["errors"])
        if "verification" in attributes:
            self.credit_card_verification = CreditCardVerification(attributes["verification"])

