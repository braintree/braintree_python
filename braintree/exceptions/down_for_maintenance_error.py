from braintree.exceptions.braintree_error import BraintreeError

class DownForMaintenanceError(BraintreeError):
    """
    Raised when the gateway is down for maintenance.

    See https://www.braintreepayments.com/docs/python/general/exceptions#down_for_maintenance_error
    """
    pass
