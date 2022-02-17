from braintree.resource import Resource

class VenmoProfileData(Resource):
    """
    A class representing Braintree VenmoProfileData object.
    """
    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)

