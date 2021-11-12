from braintree.resource import Resource

class TransactionReview(Resource):
    """
    A class representing a Transaction Review.
    """

    def __init__(self, attributes):
        Resource.__init__(self, None, attributes)
