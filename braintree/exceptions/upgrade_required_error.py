from braintree.exceptions.braintree_error import BraintreeError

class UpgradeRequiredError(BraintreeError):
    """
    Raised for unsupported client library versions.

    See https://developers.braintreepayments.com/ios+python/reference/general/exceptions#upgrade-required-error
    """
    pass
