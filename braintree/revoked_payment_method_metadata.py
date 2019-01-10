from braintree.payment_method_parser import parse_payment_method
from braintree.resource import Resource

class RevokedPaymentMethodMetadata(Resource):

    def __init__(self, gateway, attributes):
        self.revoked_payment_method = parse_payment_method(gateway, attributes)
        self.customer_id = self.revoked_payment_method.customer_id
        self.token = self.revoked_payment_method.token
