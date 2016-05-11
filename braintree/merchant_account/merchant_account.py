from braintree.configuration import Configuration
from braintree.resource import Resource
from braintree.merchant_account import BusinessDetails, FundingDetails, IndividualDetails

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
        self.individual_details = IndividualDetails(attributes.get("individual", {}))
        self.business_details = BusinessDetails(attributes.get("business", {}))
        self.funding_details = FundingDetails(attributes.get("funding", {}))
        if "master_merchant_account" in attributes:
            self.master_merchant_account = MerchantAccount(gateway, attributes.pop("master_merchant_account"))

    def __repr__(self):
        detail_list = ["id", "status", "master_merchant_account", "individual_details", "business_details", "funding_details", "default"]
        return super(MerchantAccount, self).__repr__(detail_list)

    @staticmethod
    def create(params={}):
        return Configuration.gateway().merchant_account.create(params)

    @staticmethod
    def update(id, attributes):
        return Configuration.gateway().merchant_account.update(id, attributes)

    @staticmethod
    def find(id):
        return Configuration.gateway().merchant_account.find(id)
