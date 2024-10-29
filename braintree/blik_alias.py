import braintree

from braintree.resource import Resource

class BlikAlias(Resource):
    """
    A class representing a BlikAlias.

    For more information on BlikAliases, see https://developer.paypal.com/braintree/docs/guides/local-payment-methods/blik-one-click

    """

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)

