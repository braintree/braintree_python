from braintree.resource import Resource

class ConnectedMerchantStatusTransitioned(Resource):

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
