class NotFoundError(Exception):
    """ Raised when an object is not found in the gateway, such as a Transaction.find("bad_id"). """
    pass
