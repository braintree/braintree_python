from braintree.exceptions.braintree_error import BraintreeError

class AuthorizationError(BraintreeError):
    """
    Raised when the user does not have permission to complete the requested operation.

    See https://developers.braintreepayments.com/python/reference/general/error-handling/exceptions#authorization-error
    """
    pass
