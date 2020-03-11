from braintree.exceptions.braintree_error import BraintreeError

class RequestTimeoutError(BraintreeError):
    """
    Raised when a client request timeout occurs.
    """
    pass
