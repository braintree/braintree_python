import braintree
from datetime import datetime
from braintree.resource import Resource

class AchMandate(Resource):

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        if "accepted_at" in attributes:
            self.accepted_at = datetime.strptime(attributes["accepted_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            self.accepted_at = None
