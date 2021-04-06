from braintree.resource import Resource

class LocalPaymentReversed(Resource):
    """
    A class representing Braintree LocalPaymentReversed webhook.
    """
    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)

