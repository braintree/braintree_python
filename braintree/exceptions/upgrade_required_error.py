from braintree.exceptions.braintree_error import BraintreeError

class UpgradeRequiredError(BraintreeError):
    """ Raised for unsupported client library versions. """
    pass
