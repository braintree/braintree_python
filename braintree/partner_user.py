from braintree.configuration import Configuration
from braintree.resource import Resource

class PartnerUser(Resource):

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        if "partner_user_id" in attributes:
            self.partner_user_id = attributes.pop("partner_user_id")
        if "private_key" in attributes:
            self.private_key = attributes.pop("private_key")
        if "public_key" in attributes:
            self.public_key = attributes.pop("public_key")
        if "merchant_public_id" in attributes:
            self.merchant_public_id = attributes.pop("merchant_public_id")

    def __repr__(self):
        detail_list = ["partner_user_id", "public_key", "private_key", "merchant_public_id"]
        return super.__repr__(detail_list)
