import braintree
import urllib
import warnings
from decimal import Decimal
from braintree.add_on import AddOn
from braintree.discount import Discount
from braintree.successful_result import SuccessfulResult
from braintree.status_event import StatusEvent
from braintree.error_result import ErrorResult
from braintree.resource import Resource
from braintree.address import Address
from braintree.configuration import Configuration
from braintree.credit_card import CreditCard
from braintree.customer import Customer
from braintree.subscription_details import SubscriptionDetails
from braintree.resource_collection import ResourceCollection
from braintree.transparent_redirect import TransparentRedirect
from braintree.exceptions.not_found_error import NotFoundError
from braintree.descriptor import Descriptor

class Transaction(Resource):
    """
    A class representing Braintree Transaction objects.

    An example of creating an sale transaction with all available fields::

        result = Transaction.sale({
            "amount": "100.00",
            "order_id": "123",
            "credit_card": {
                "number": "5105105105105100",
                "expiration_date": "05/2011",
                "cvv": "123"
            },
            "customer": {
                "first_name": "Dan",
                "last_name": "Smith",
                "company": "Braintree Payment Solutions",
                "email": "dan@example.com",
                "phone": "419-555-1234",
                "fax": "419-555-1235",
                "website": "http://braintreepayments.com"
            },
            "billing": {
                "first_name": "Carl",
                "last_name": "Jones",
                "company": "Braintree",
                "street_address": "123 E Main St",
                "extended_address": "Suite 403",
                "locality": "Chicago",
                "region": "IL",
                "postal_code": "60622",
                "country_name": "United States of America"
            },
            "shipping": {
                "first_name": "Andrew",
                "last_name": "Mason",
                "company": "Braintree",
                "street_address": "456 W Main St",
                "extended_address": "Apt 2F",
                "locality": "Bartlett",
                "region": "IL",
                "postal_code": "60103",
                "country_name": "United States of America"
            }
        })

        print(result.transaction.amount)
        print(result.transaction.order_id)

    For more information on Transactions, see http://www.braintreepayments.com/gateway/transaction-api
    """

    class CreatedUsing(object):
        """
        Constants representing how the transaction was created.  Available types are:

        * braintree.Transaction.CreatedUsing.FullInformation
        * braintree.Transaction.CreatedUsing.Token
        """

        FullInformation = "full_information"
        Token = "token"

    class GatewayRejectionReason(object):
        """
        Constants representing gateway rejection reasons. Available types are:

        * braintree.Transaction.GatewayRejectionReason.Avs
        * braintree.Transaction.GatewayRejectionReason.AvsAndCvv
        * braintree.Transaction.GatewayRejectionReason.Cvv
        * braintree.Transaction.GatewayRejectionReason.Duplicate
        """
        Avs = "avs"
        AvsAndCvv = "avs_and_cvv"
        Cvv = "cvv"
        Duplicate = "duplicate"

    class Source(object):
        Api = "api"
        ControlPanel = "control_panel"
        Recurring = "recurring"

    class Status(object):
        """
        Constants representing transaction statuses. Available statuses are:

        * braintree.Transaction.Status.Authorized
        * braintree.Transaction.Status.Authorizing
        * braintree.Transaction.Status.Failed
        * braintree.Transaction.Status.GatewayRejected
        * braintree.Transaction.Status.ProcessorDeclined
        * braintree.Transaction.Status.Settled
        * braintree.Transaction.Status.SettlementFailed
        * braintree.Transaction.Status.SubmittedForSettlement
        * braintree.Transaction.Status.Void
        """

        AuthorizationExpired   = "authorization_expired"
        Authorized             = "authorized"
        Authorizing            = "authorizing"
        Failed                 = "failed"
        GatewayRejected        = "gateway_rejected"
        ProcessorDeclined      = "processor_declined"
        Settled                = "settled"
        SettlementFailed       = "settlement_failed"
        SubmittedForSettlement = "submitted_for_settlement"
        Voided                 = "voided"

    class Type(object):
        """
        Constants representing transaction types. Available types are:

        * braintree.Transaction.Type.Credit
        * braintree.Transaction.Type.Sale
        """

        Credit = "credit"
        Sale = "sale"

    @staticmethod
    def clone_transaction(transaction_id, params):
        return Configuration.gateway().transaction.clone_transaction(transaction_id, params)

    @staticmethod
    def confirm_transparent_redirect(query_string):
        """
        Confirms a transparent redirect request. It expects the query string from the
        redirect request. The query string should _not_ include the leading "?" character. ::

            result = braintree.Transaction.confirm_transparent_redirect_request("foo=bar&id=12345")
        """

        warnings.warn("Please use TransparentRedirect.confirm instead", DeprecationWarning)
        return Configuration.gateway().transaction.confirm_transparent_redirect(query_string)

    @staticmethod
    def credit(params={}):
        """
        Creates a transaction of type Credit. Amount is required. Also, a credit card,
        customer_id or payment_method_token is required. ::

            result = braintree.Transaction.credit({
                "amount": "100.00",
                "payment_method_token": "my_token"
            })

            result = braintree.Transaction.credit({
                "amount": "100.00",
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "12/2012"
                }
            })

            result = braintree.Transaction.credit({
                "amount": "100.00",
                "customer_id": "my_customer_id"
            })
        """

        params["type"] = Transaction.Type.Credit
        return Transaction.create(params)

    @staticmethod
    def find(transaction_id):
        """
        Find a transaction, given a transaction_id. This does not return
        a result object. This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>` if the provided
        credit_card_id is not found. ::

            transaction = braintree.Transaction.find("my_transaction_id")
        """
        return Configuration.gateway().transaction.find(transaction_id)


    @staticmethod
    def refund(transaction_id, amount=None):
        """
        Refunds an existing transaction. It expects a transaction_id. ::

            result = braintree.Transaction.refund("my_transaction_id")
        """

        return Configuration.gateway().transaction.refund(transaction_id, amount)


    @staticmethod
    def sale(params={}):
        """
        Creates a transaction of type Sale. Amount is required. Also, a credit card,
        customer_id or payment_method_token is required. ::

            result = braintree.Transaction.sale({
                "amount": "100.00",
                "payment_method_token": "my_token"
            })

            result = braintree.Transaction.sale({
                "amount": "100.00",
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "12/2012"
                }
            })

            result = braintree.Transaction.sale({
                "amount": "100.00",
                "customer_id": "my_customer_id"
            })
        """

        params["type"] = Transaction.Type.Sale
        return Transaction.create(params)

    @staticmethod
    def search(*query):
        return Configuration.gateway().transaction.search(*query)

    @staticmethod
    def submit_for_settlement(transaction_id, amount=None):
        """
        Submits an authorized transaction for settlement. ::

            result = braintree.Transaction.submit_for_settlement("my_transaction_id")
        """

        return Configuration.gateway().transaction.submit_for_settlement(transaction_id, amount)

    @staticmethod
    def tr_data_for_credit(tr_data, redirect_url):
        """
        Builds tr_data for a Transaction of type Credit
        """
        return Configuration.gateway().transaction.tr_data_for_credit(tr_data, redirect_url)

    @staticmethod
    def tr_data_for_sale(tr_data, redirect_url):
        """
        Builds tr_data for a Transaction of type Sale
        """
        return Configuration.gateway().transaction.tr_data_for_sale(tr_data, redirect_url)

    @staticmethod
    def transparent_redirect_create_url():
        """
        Returns the url to be used for creating Transactions through transparent redirect.
        """

        warnings.warn("Please use TransparentRedirect.url instead", DeprecationWarning)
        return Configuration.gateway().transaction.transparent_redirect_create_url()

    @staticmethod
    def void(transaction_id):
        """
        Voids an existing transaction. It expects a transaction_id. ::

            result = braintree.Transaction.void("my_transaction_id")
        """

        return Configuration.gateway().transaction.void(transaction_id)

    @staticmethod
    def create(params):
        """
        Creates a transaction. Amount and type are required. Also, a credit card,
        customer_id or payment_method_token is required. ::

            result = braintree.Transaction.sale({
                "type": braintree.Transaction.Type.Sale,
                "amount": "100.00",
                "payment_method_token": "my_token"
            })

            result = braintree.Transaction.sale({
                "type": braintree.Transaction.Type.Sale,
                "amount": "100.00",
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "12/2012"
                }
            })

            result = braintree.Transaction.sale({
                "type": braintree.Transaction.Type.Sale,
                "amount": "100.00",
                "customer_id": "my_customer_id"
            })
        """
        return Configuration.gateway().transaction.create(params)

    @staticmethod
    def clone_signature():
        return ["amount", {"options": ["submit_for_settlement"]}]

    @staticmethod
    def create_signature():
        return [
            "amount", "customer_id", "merchant_account_id", "order_id", "payment_method_token", "purchase_order_number", "shipping_address_id", "tax_amount", "tax_exempt", "type",
            {
                "credit_card": [
                    "token", "cardholder_name", "cvv", "expiration_date", "expiration_month", "expiration_year", "number"
                ]
            },
            {
                "customer": [
                    "id", "company", "email", "fax", "first_name", "last_name", "phone", "website"
                ]
            },
            {
                "billing": [
                    "first_name", "last_name", "company", "country_code_alpha2", "country_code_alpha3",
                    "country_code_numeric", "country_name", "extended_address", "locality",
                    "postal_code", "region", "street_address"
                ]
            },
            {
                "shipping": [
                    "first_name", "last_name", "company", "country_code_alpha2", "country_code_alpha3",
                    "country_code_numeric", "country_name", "extended_address", "locality",
                    "postal_code", "region", "street_address"
                ]
            },
            {
                "options": [
                    "store_in_vault", "store_in_vault_on_success", "submit_for_settlement",
                    "add_billing_address_to_payment_method", "store_shipping_address_in_vault"
                ]
            },
            {"custom_fields": ["__any_key__"]},
            {"descriptor": ["name", "phone"]}
        ]

    def __init__(self, gateway, attributes):
        if "refund_id" in attributes.keys():
            self._refund_id = attributes["refund_id"]
            del(attributes["refund_id"])
        else:
            self._refund_id = None

        Resource.__init__(self, gateway, attributes)

        self.amount = Decimal(self.amount)
        if self.tax_amount:
            self.tax_amount = Decimal(self.tax_amount)
        if "billing" in attributes:
            self.billing_details = Address(gateway, attributes.pop("billing"))
        if "credit_card" in attributes:
            self.credit_card_details = CreditCard(gateway, attributes.pop("credit_card"))
        if "customer" in attributes:
            self.customer_details = Customer(gateway, attributes.pop("customer"))
        if "shipping" in attributes:
            self.shipping_details = Address(gateway, attributes.pop("shipping"))
        if "add_ons" in attributes:
            self.add_ons = [AddOn(gateway, add_on) for add_on in self.add_ons]
        if "discounts" in attributes:
            self.discounts = [Discount(gateway, discount) for discount in self.discounts]
        if "status_history" in attributes:
            self.status_history = [StatusEvent(gateway, status_event) for status_event in self.status_history]
        if "subscription" in attributes:
            self.subscription_details = SubscriptionDetails(attributes.pop("subscription"))
        if "descriptor" in attributes:
            self.descriptor = Descriptor(gateway, attributes.pop("descriptor"))

    @property
    def refund_id(self):
        warnings.warn("Please use Transaction.refund_ids instead", DeprecationWarning)
        return self._refund_id

    @property
    def vault_billing_address(self):
        """
        The vault billing address associated with this transaction
        """

        return self.gateway.address.find(self.customer_details.id, self.billing_details.id)

    @property
    def vault_credit_card(self):
        """
        The vault credit card associated with this transaction
        """
        if self.credit_card_details.token is None:
            return None
        return self.gateway.credit_card.find(self.credit_card_details.token)

    @property
    def vault_customer(self):
        """
        The vault customer associated with this transaction
        """
        if self.customer_details.id is None:
            return None
        return self.gateway.customer.find(self.customer_details.id)
