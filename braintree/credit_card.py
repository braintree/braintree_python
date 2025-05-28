import braintree
import warnings
from braintree.resource import Resource
from braintree.address import Address
from braintree.configuration import Configuration
from braintree.credit_card_verification import CreditCardVerification
from enum import Enum

class CreditCard(Resource):
    """
    A class representing Braintree CreditCard objects.

    An example of creating an credit card with all available fields::

        result = braintree.CreditCard.create({
            "cardholder_name": "John Doe",
            "cvv": "123",
            "expiration_date": "12/2012",
            "number": "4111111111111111",
            "token": "my_token",
            "billing_address": {
                "first_name": "John",
                "last_name": "Doe",
                "company": "Braintree",
                "street_address": "111 First Street",
                "extended_address": "Unit 1",
                "locality": "Chicago",
                "postal_code": "60606",
                "region": "IL",
                "country_name": "United States of America"
                "phone_number": "312-123-4567"
            },
            "options": {
                "verify_card": True,
                "verification_amount": "2.00"
            }
        })

        print(result.credit_card.token)
        print(result.credit_card.masked_number)

    For more information on CreditCards, see https://developer.paypal.com/braintree/docs/reference/request/credit-card/create/python

    """
    class CardType(object):
        """
        Contants representing the type of the credit card.  Available types are:

        * Braintree.CreditCard.AmEx
        * Braintree.CreditCard.CarteBlanche
        * Braintree.CreditCard.ChinaUnionPay
        * Braintree.CreditCard.DinersClubInternational
        * Braintree.CreditCard.Discover
        * Braintree.CreditCard.Electron
        * Braintree.CreditCard.Elo
        * Braintree.CreditCard.Hiper
        * Braintree.CreditCard.Hipercard
        * Braintree.CreditCard.JCB
        * Braintree.CreditCard.Laser
        * Braintree.CreditCard.UK_Maestro
        * Braintree.CreditCard.Maestro
        * Braintree.CreditCard.MasterCard
        * Braintree.CreditCard.Solo
        * Braintree.CreditCard.Switch
        * Braintree.CreditCard.Visa
        * Braintree.CreditCard.Unknown
        """

        AmEx = "American Express"
        CarteBlanche = "Carte Blanche"
        ChinaUnionPay = "China UnionPay"
        DinersClubInternational = "Diners Club"
        Discover = "Discover"
        Electron = "Electron"
        Elo = "Elo"
        Hiper = "Hiper"
        Hipercard = "Hipercard"
        JCB = "JCB"
        Laser = "Laser"
        UK_Maestro = "UK Maestro"
        Maestro = "Maestro"
        MasterCard = "MasterCard"
        Solo = "Solo"
        Switch = "Switch"
        Visa = "Visa"
        Unknown = "Unknown"

    class CustomerLocation(object):
        """
        Contants representing the issuer location of the credit card.  Available locations are:

        * braintree.CreditCard.CustomerLocation.International
        * braintree.CreditCard.CustomerLocation.US
        """

        International = "international"
        US = "us"

    # NEXT_MAJOR_VERSION this can be an enum! they were added as of python 3.4 and we support 3.5+
    class CardTypeIndicator(object):
        """
        Constants representing the three states for the card type indicator attributes

        * braintree.CreditCard.CardTypeIndicator.Yes
        * braintree.CreditCard.CardTypeIndicator.No
        * braintree.CreditCard.CardTypeIndicator.Unknown
        """
        Yes = "Yes"
        No = "No"
        Unknown = "Unknown"

    class DebitNetwork(Enum):
        """
        Constants representing the debit networks used for processing a pinless debit transaction

        * braintree.CreditCard.DebitNetwork.Accel
        * braintree.CreditCard.DebitNetwork.Maestro
        * braintree.CreditCard.DebitNetwork.Nyce
        * braintree.CreditCard.DebitNetwork.Pulse
        * braintree.CreditCard.DebitNetwork.Star
        * braintree.CreditCard.DebitNetwork.Star_Access
        """
        Accel = "ACCEL"
        Maestro= "MAESTRO"
        Nyce = "NYCE"
        Pulse = "PULSE"
        Star = "STAR"
        Star_Access = "STAR_ACCESS"

    Commercial = CountryOfIssuance = Debit = DurbinRegulated = \
            Business = Consumer = Corporate = Purchase = \
            Healthcare = IssuingBank = Payroll = Prepaid = PrepaidReloadable = ProductId = CardTypeIndicator

    @staticmethod
    def create(params=None):
        """
        Create a CreditCard.

        A number and expiration_date are required. ::

            result = braintree.CreditCard.create({
                "number": "4111111111111111",
                "expiration_date": "12/2012"
            })

        """
        if params is None:
            params = {}
        return Configuration.gateway().credit_card.create(params)

    @staticmethod
    def update(credit_card_token, params=None):
        """
        Update an existing CreditCard

        By credit_card_id.  The params are similar to create::

            result = braintree.CreditCard.update("my_credit_card_id", {
                "cardholder_name": "John Doe"
            })

        """
        if params is None:
            params = {}
        return Configuration.gateway().credit_card.update(credit_card_token, params)

    @staticmethod
    def delete(credit_card_token):
        """
        Delete a credit card

        Given a credit_card_id::

            result = braintree.CreditCard.delete("my_credit_card_id")

        """

        return Configuration.gateway().credit_card.delete(credit_card_token)

    @staticmethod
    def expired():
        """ Return a collection of expired credit cards. """
        return Configuration.gateway().credit_card.expired()

    @staticmethod
    def expiring_between(start_date, end_date):
        """ Return a collection of credit cards expiring between the given dates. """
        return Configuration.gateway().credit_card.expiring_between(start_date, end_date)

    @staticmethod
    def find(credit_card_token):
        """
        Find a credit card, given a credit_card_id. This does not return
        a result object. This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>` if the provided
        credit_card_id is not found. ::

            credit_card = braintree.CreditCard.find("my_credit_card_token")
        """
        return Configuration.gateway().credit_card.find(credit_card_token)

    @staticmethod
    def from_nonce(nonce):
        """
        Convert a payment method nonce into a CreditCard. This does not return
        a result object. This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>` if the provided
        credit_card_id is not found. ::

            credit_card = braintree.CreditCard.from_nonce("my_payment_method_nonce")
        """
        return Configuration.gateway().credit_card.from_nonce(nonce)

    @staticmethod
    def create_signature():
        return CreditCard.signature("create")

    @staticmethod
    def update_signature():
        return CreditCard.signature("update")

    @staticmethod
    def signature(type):
        billing_address_params = [
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
            "region",
            "street_address",
            "phone_number"
        ]

        options = [
            "account_information_inquiry",
            "fail_on_duplicate_payment_method",
            "fail_on_duplicate_payment_method_for_customer",
            "make_default",
            "skip_advanced_fraud_checking",
            "venmo_sdk_session",  # NEXT_MJOR_VERSION remove venmo_sdk_session
            "verification_account_type",
            "verification_amount",
            "verification_merchant_account_id",
            "verify_card",
            {
                "adyen":[
                    "overwrite_brand",
                    "selected_brand"
                ]
            }
        ]

        three_d_secure_pass_thru = [
            "cavv",
            "ds_transaction_id",
            "eci_flag",
            "three_d_secure_version",
            "xid"
        ]

        signature = [
            "billing_address_id",
            "cardholder_name",
            "cvv",
            "expiration_date",
            "expiration_month",
            "expiration_year",
            "number",
            "token",
            "venmo_sdk_payment_method_code", # NEXT_MJOR_VERSION remove venmo_sdk_payment_method_code
            "device_data",
            "payment_method_nonce",
            "device_session_id", "fraud_merchant_id", # NEXT_MAJOR_VERSION remove device_session_id and fraud_merchant_id
            {
                "billing_address": billing_address_params
            },
            {
                "options": options
            },
            {
                "three_d_secure_pass_thru": three_d_secure_pass_thru
            }
        ]

        if type == "create":
            signature.append("customer_id")
        elif type == "update":
            billing_address_params.append({"options": ["update_existing"]})
        elif type == "update_via_customer":
            options.append("update_existing_token")
            billing_address_params.append({"options": ["update_existing"]})
        else:
            raise AttributeError

        return signature

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        self.is_expired = self.expired
        if "billing_address" in attributes:
            self.billing_address = Address(gateway, self.billing_address)
        else:
            self.billing_address = None

        if "subscriptions" in attributes:
            self.subscriptions = [braintree.subscription.Subscription(gateway, subscription) for subscription in self.subscriptions]

        if "verifications" in attributes:
            sorted_verifications = sorted(attributes["verifications"], key=lambda verification: verification["created_at"], reverse=True)
            if len(sorted_verifications) > 0:
                self.verification = CreditCardVerification(gateway, sorted_verifications[0])

    @property
    def expiration_date(self):
        if not self.expiration_month or not self.expiration_year:
            return None
        return self.expiration_month + "/" + self.expiration_year

    @property
    def masked_number(self):
        """
        Returns the masked number of the CreditCard.
        """
        bin = self.bin_extended if hasattr(self, "bin_extended") else self.bin
        mask_length = 16 - len(bin) - len(self.last_4)
        mask = "*" * mask_length
        return bin + mask + self.last_4
