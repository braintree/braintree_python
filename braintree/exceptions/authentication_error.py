from braintree.exceptions.braintree_error import BraintreeError

class AuthenticationError(BraintreeError):
    """
    Raised when the client library cannot authenticate with the gateway.  This generally means the public_key/private key are incorrect, or the user is not active.

    See https://developer.paypal.com/braintree/docs/reference/general/exceptions/python#authentication-error
    """
    pass
