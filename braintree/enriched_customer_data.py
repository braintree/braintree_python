from braintree.resource import Resource
from braintree.venmo_profile_data import VenmoProfileData

class EnrichedCustomerData(Resource):
    """
    A class representing Braintree EnrichedCustomerData object.
    """
    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        self.profile_data = VenmoProfileData(gateway, attributes.pop("profile_data"))
