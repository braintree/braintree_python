from braintree.exceptions.braintree_error import BraintreeError

class ForgedQueryStringError(BraintreeError):
    """
    Raised when the query string has been forged or tampered with during a transparent redirect.

    See http://www.braintreepayments.com/docs/python/general/exceptions#forged_query_string
    """
    pass
