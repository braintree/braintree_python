class ForgedQueryStringError(Exception):
    """ Raised when the query string has been forged or tampered with during a transparent redirect. """
    pass
