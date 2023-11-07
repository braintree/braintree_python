import braintree
from braintree.address import Address
from braintree.resource import Resource

class MetaCheckoutToken(Resource):
    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)

    @property
    def expiration_date(self):
        if not self.expiration_month or not self.expiration_year:
            return None
        return self.expiration_month + "/" + self.expiration_year

    @property
    def masked_number(self):
        return self.bin + "******" + self.last_4
