import braintree
from braintree.util.datetime_parser import parse_datetime
from braintree.resource import Resource

class AchMandate(Resource):

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        if "accepted_at" in attributes:
            self.accepted_at = parse_datetime(attributes["accepted_at"])
        else:
            self.accepted_at = None
