class AuthenticationError(Exception):
    """
    Raised when the client library cannot authenticate with the gateway.  This generally means the public_key/private key are incorrect, or the user is not active.
    """
    pass
