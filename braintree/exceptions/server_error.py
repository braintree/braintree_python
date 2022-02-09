from braintree.exceptions.braintree_error import BraintreeError

class ServerError(BraintreeError):
    """
    Raised when the gateway raises an error.  Please contact support at support@getbraintree.com.

    See https://developer.paypal.com/braintree/docs/reference/general/exceptions/python#server-error
    """
    pass
