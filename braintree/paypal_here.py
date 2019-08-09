import braintree
from braintree.resource import Resource

class PayPalHere(Resource):
    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)

