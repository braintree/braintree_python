from braintree.exceptions.braintree_error import BraintreeError

class GatewayTimeoutError(BraintreeError):
    """
    Raised when a gateway response timeout occurs.
    """
    pass
