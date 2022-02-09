from braintree.exceptions.braintree_error import BraintreeError

class UpgradeRequiredError(BraintreeError):
    """
    Raised for unsupported client library versions.

    See https://developer.paypal.com/braintree/docs/reference/general/exceptions/python#upgrade-required-error
    """
    pass
