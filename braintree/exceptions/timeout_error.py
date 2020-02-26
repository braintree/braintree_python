from braintree.exceptions.braintree_error import BraintreeError

class TimeoutError(BraintreeError):
    """
    Raised when a Timeout occurs
    """
    pass
