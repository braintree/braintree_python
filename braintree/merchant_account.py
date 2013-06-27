from braintree.resource import Resource

class MerchantAccount(Resource):
    class Status(object):
        Active = "active"
        Pending = "pending"
        Suspended = "suspended"

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        if "master_merchant_account" in attributes:
            self.master_merchant_account = MerchantAccount(gateway, self.master_merchant_account)

    @staticmethod
    def create_signature():
        return CreditCard.signature("create")

    @staticmethod
    def signature(type):
        signature = [
            {'applicant_details': [
                'first_name', 'last_name', 'email', 'date_of_birth', 'ssn', 'routing_number', 'account_number',
                {'address': ['street_address', 'postal_code', 'locality', 'region']}]
            },
            'tos_accepted', 'master_merchant_account_id', 'id'
        ]

        return signature
