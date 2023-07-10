import braintree
from braintree.resource import Resource

class ApplePayCard(Resource):
    """
    A class representing Braintree Apple Pay card objects.
    """
    class CardType(object):
        """
        Contants representing the type of the credit card.  Available types are:

        * Braintree.ApplePayCard.AmEx
        * Braintree.ApplePayCard.MasterCard
        * Braintree.ApplePayCard.Visa
        """

        AmEx = "Apple Pay - American Express"
        MasterCard = "Apple Pay - MasterCard"
        Visa = "Apple Pay - Visa"

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        if hasattr(self, 'expired'):
            self.is_expired = self.expired

        if "subscriptions" in attributes:
            self.subscriptions = [braintree.subscription.Subscription(gateway, subscription) for subscription in self.subscriptions]

    @property
    def expiration_date(self):
        if not self.expiration_month or not self.expiration_year:
            return None
        return self.expiration_month + "/" + self.expiration_year

    @staticmethod
    def signature():
        options = ["make_default"]

        signature = [
            "customer_id",
            "cardholder_name",
            "expiration_month",
            "expiration_year",
            "number",
            "cryptogram",
            "eci_indicator",
            "token",
            {
                "options": options
            },
            {
                "billing_address": [
                    "company",
                    "country_code_alpha2",
                    "country_code_alpha3",
                    "country_code_numeric",
                    "country_name",
                    "extended_address",
                    "first_name",
                    "last_name",
                    "locality",
                    "postal_code",
                    "phone_number",
                    "region",
                    "street_address"
                ]
            }
        ]

        return signature

