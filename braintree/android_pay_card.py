import braintree
from braintree.resource import Resource

# NEXT_MAJOR_VERSION - rename to GooglePayCard
class AndroidPayCard(Resource):
    """
    A class representing Braintree Android Pay card objects.
    """
    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        if hasattr(self, 'expired'):
            self.is_expired = self.expired

        if "subscriptions" in attributes:
            self.subscriptions = [braintree.subscription.Subscription(gateway, subscription) for subscription in self.subscriptions]

    @property
    def expiration_date(self):
        return self.expiration_month + "/" + self.expiration_year

    @property
    def last_4(self):
        return self.virtual_card_last_4

    @property
    def card_type(self):
        return self.virtual_card_type

    @property
    def bin(self):
        return self.bin

    @property
    def token(self):
        return self.token

    @property
    def commercial(self):
        return self.commercial

    @property
    def country_of_issuance(self):
        return self.country_of_issuance

    @property
    def debit(self):
        return self.debit

    @property
    def durbin_regulated(self):
        return self.durbin_regulated

    @property
    def healthcare(self):
        return self.healthcare

    @property
    def issuing_bank(self):
        return self.issuing_bank

    @property
    def payroll(self):
        return self.payroll

    @property
    def prepaid(self):
        return self.prepaid

    @property
    def product_id(self):
        return self.product_id
