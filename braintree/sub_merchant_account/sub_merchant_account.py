from braintree.configuration import Configuration
from braintree.resource import Resource
from braintree.sub_merchant_account import ContactDetails,  BusinessDetails, FundingDetails

class SubMerchantAccount(Resource):
    class Status(object):
        Pending = "pending"

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        self.business_details = BusinessDetails(attributes.get("business", {}))
        self.funding_details = FundingDetails(attributes.get("funding", {}))
        self.contacts = self._build_contacts(attributes)

    def __repr__(self):
        detail_list = [
            "id",
            "tos_accepted",
            "contacts",
            "business_details",
            "funding_details",
        ]

        return super(SubMerchantAccount, self).__repr__(detail_list)

    def _build_contacts(self, attributes):
        contacts = []
        for contact_attributes in attributes.get("contacts", []):
            contacts.append(ContactDetails(contact_attributes))

        return contacts

    @staticmethod
    def create(params={}):
        return Configuration.gateway().sub_merchant_account.create(params)

    @staticmethod
    def update(sub_merchant_account_id, params={}):
        return Configuration.gateway().sub_merchant_account.update(sub_merchant_account_id, params)
