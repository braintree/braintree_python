from braintree.exceptions.braintree_error import BraintreeError

class DownForMaintenanceError(BraintreeError):
    """ Raised when the gateway is down for maintenance. """
    pass
