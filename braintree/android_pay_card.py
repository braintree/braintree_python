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
        return self.virtual_bin

    @property
    def token(self):
        return self.virtual_token

    @property
    def commercial(self):
        return self.virtual_commercial

    @property
    def country_of_issuance(self):
        return self.virtual_country_of_issuance

    @property
    def debit(self):
        return self.virtual_debit

    @property
    def durbin_regulated(self):
        return self.virtual_durbin_regulated

    @property
    def healthcare(self):
        return self.virtual_healthcare

    @property
    def issuing_bank(self):
        return self.virtual_issuing_bank

    @property
    def payroll(self):
        return self.virtual_payroll

    @property
    def prepaid(self):
        return self.virtual_prepaid

    @property
    def product_id(self):
        return self.virtual_product_id
