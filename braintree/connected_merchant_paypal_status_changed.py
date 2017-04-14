from braintree.resource import Resource

class ConnectedMerchantPayPalStatusChanged(Resource):

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
