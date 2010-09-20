import braintree
from braintree.errors import Errors
from braintree.credit_card_verification import CreditCardVerification

class ErrorResult(object):
    """
    An instance of this class is returned from most operations when there is a validation error.  Call :func:`errors` to get the collection of errors::

        error_result = Transaction.sale({})
        assert(error_result.is_success == False)
        assert(error_result.errors.for_object("transaction").on("amount")[0].code == ErrorCodes.Transaction.AmountIsRequired)

    Errors can be nested at different levels.  For example, creating a transaction with a credit card can have errors at the transaction level as well as the credit card level.  :func:`for_object` returns the :class:`ValidationErrorCollection <braintree.validation_error_collection.ValidationErrorCollection>` for the errors at that level.  For example::

        error_result = Transaction.sale({"credit_card": {"number": "invalid"}})
        assert(error_result.errors.for_object("transaction").for_object("credit_card").on("number")[0].code == ErrorCodes.CreditCard.NumberHasInvalidLength)
    """

    def __init__(self, gateway, attributes):
        self.params = attributes["params"]
        self.errors = Errors(attributes["errors"])
        self.message = attributes["message"]

        if "verification" in attributes:
            self.credit_card_verification = CreditCardVerification(gateway, attributes["verification"])
        else:
            self.credit_card_verification = None

        if "transaction" in attributes:
            self.transaction = braintree.transaction.Transaction(gateway, attributes["transaction"])
        else:
            self.transaction = None

        if "subscription" in attributes:
            self.subscription = braintree.subscription.Subscription(gateway, attributes["subscription"])
        else:
            self.subscription = None


    @property
    def is_success(self):
        """ Returns whether the result from the gateway is a successful response. """

        return False
