from braintree.exceptions.braintree_error import BraintreeError

class DownForMaintenanceError(BraintreeError):
    """
    Raised when the gateway is down for maintenance.

    See https://developers.braintreepayments.com/ios+python/reference/general/exceptions#down-for-maintenance
    """
    pass
