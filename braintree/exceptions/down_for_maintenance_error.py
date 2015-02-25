from braintree.exceptions.braintree_error import BraintreeError

class DownForMaintenanceError(BraintreeError):
    """
    Raised when the gateway is down for maintenance.

    See https://developers.braintreepayments.com/python/reference/general/error-handling/exceptions#down-for-maintenance-error
    """
    pass
