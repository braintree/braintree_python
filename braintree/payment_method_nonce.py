from braintree.resource import Resource
from braintree.configuration import Configuration
from braintree.three_d_secure_info import ThreeDSecureInfo
from braintree.bin_data import BinData

class PaymentMethodNonce(Resource):
    @staticmethod
    def create(payment_method_token, params = {}):
        return Configuration.gateway().payment_method_nonce.create(payment_method_token, params)

    @staticmethod
    def find(payment_method_nonce):
        return Configuration.gateway().payment_method_nonce.find(payment_method_nonce)

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)

        if "three_d_secure_info" in attributes and attributes["three_d_secure_info"] is not None:
            self.three_d_secure_info = ThreeDSecureInfo(attributes["three_d_secure_info"])
        else:
            self.three_d_secure_info = None

        if "authentication_insight" in attributes and attributes["authentication_insight"] is not None:
            self.authentication_insight = attributes["authentication_insight"]
        else:
            self.authentication_insight = None

        if "bin_data" in attributes and attributes["bin_data"] is not None:
            self.bin_data = BinData(attributes["bin_data"])
        else:
            self.bin_data = None
