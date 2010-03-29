from braintree.errors import Errors
from braintree.credit_card_verification import CreditCardVerification

class ErrorResult(object):
    """
    An instance of this class is returned from most operations when there is a validation error.  Call :func:`errors` to get the collection of errors::

        result = Transaction.sale({})
        assert(result.is_success == False)
        assert(result.errors.for_object("transaction").on("amount")[0].code == ErrorCodes.Transaction.AmountIsRequired)
    """

    def __init__(self, attributes):
        self.params = attributes["params"]
        self.errors = Errors(attributes["errors"])
        if "verification" in attributes:
            self.credit_card_verification = CreditCardVerification(attributes["verification"])

    @property
    def is_success(self):
        return False
