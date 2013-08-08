from braintree.configuration import Configuration
from braintree.resource import Resource

class MerchantAccount(Resource):
    class Status(object):
        Active = "active"
        Pending = "pending"
        Suspended = "suspended"

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        if "master_merchant_account" in attributes:
            self.master_merchant_account = MerchantAccount(gateway, attributes.pop("master_merchant_account"))

    def __repr__(self):
        detail_list = ["id", "status", "master_merchant_account"]
        return super(Address, self).__repr__(detail_list)

    @staticmethod
    def create(params={}):
        return Configuration.gateway().merchant_account.create(params)

    @staticmethod
    def create_signature():
        signature = [
            {'applicant_details': [
                'company_name',
                'first_name',
                'last_name',
                'email',
                'phone',
                'date_of_birth',
                'ssn',
                'tax_id',
                'routing_number',
                'account_number',
                {'address': [
                    'street_address',
                    'postal_code',
                    'locality',
                    'region']}
                ]
            },
            'tos_accepted',
            'master_merchant_account_id',
            'id'
        ]

        return signature
