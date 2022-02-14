from braintree.exceptions.braintree_error import BraintreeError

class NotFoundError(BraintreeError):
    """
    Raised when an object is not found in the gateway, such as a Transaction.find("bad_id").

    See https://developer.paypal.com/braintree/docs/reference/general/exceptions/python#not-found-error
    """
    pass
