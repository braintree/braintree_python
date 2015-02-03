from braintree.exceptions.braintree_error import BraintreeError

class UpgradeRequiredError(BraintreeError):
    """
    Raised for unsupported client library versions.

    See https://developers.braintreepayments.com/python/reference/general/error-handling/exceptions#upgrade-required-error
    """
    pass
