from braintree.exceptions.braintree_error import BraintreeError

class UpgradeRequiredError(BraintreeError):
    """
    Raised for unsupported client library versions.

    See http://www.braintreepayments.com/docs/python/general/exceptions#upgrade_required_error
    """
    pass
