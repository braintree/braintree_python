from braintree.configuration import Configuration
from braintree.resource import Resource

class MerchantAccount(Resource):
    class Status(object):
        Active = "active"
        Pending = "pending"
        Suspended = "suspended"
        
    class FundingDestination(object):
        Bank = "bank"
        Email = "email"
        MobilePhone = "mobile_phone"
    FundingDestinations = FundingDestination

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)

    def __repr__(self):
        detail_list = [
            "id",
            "currency_iso_code",
            "default",
            "status",
        ]
        return super(MerchantAccount, self).__repr__(detail_list)

    @staticmethod
    def create(params=None):
        if params is None:
            params = {}
        return Configuration.gateway().merchant_account.create(params)

    @staticmethod
    def update(id, attributes):
        return Configuration.gateway().merchant_account.update(id, attributes)

    @staticmethod
    def find(id):
        return Configuration.gateway().merchant_account.find(id)