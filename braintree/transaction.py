import braintree
import warnings
from decimal import Decimal
from braintree.add_on import AddOn
from braintree.disbursement_detail import DisbursementDetail
from braintree.dispute import Dispute
from braintree.discount import Discount
from braintree.successful_result import SuccessfulResult
from braintree.status_event import StatusEvent
from braintree.error_result import ErrorResult
from braintree.resource import Resource
from braintree.address import Address
from braintree.configuration import Configuration
from braintree.credit_card import CreditCard
from braintree.customer import Customer
from braintree.paypal_account import PayPalAccount
from braintree.sepa_bank_account import SEPABankAccount
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
            "channel": "MyShoppingCartProvider",
            "credit_card": {
                "number": "5105105105105100",
                "expiration_date": "05/2011",
                "cvv": "123"
            },
            "customer": {
                "first_name": "Dan",
                "last_name": "Smith",
                "company": "Braintree",
                "email": "dan@example.com",
                "phone": "419-555-1234",
                "fax": "419-555-1235",
                "website": "https://www.braintreepayments.com"
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

    For more information on Transactions, see https://www.braintreepayments.com/docs/python/transactions/create

    """

    def __repr__(self):
        detail_list = ["amount", "credit_card", "payment_method_token", "customer_id"]
        return super(Transaction, self).__repr__(detail_list)

    class CreatedUsing(object):
        """
        Constants representing how the transaction was created.  Available types are:

        * braintree.Transaction.CreatedUsing.FullInformation
        * braintree.Transaction.CreatedUsing.Token
        """

        FullInformation = "full_information"
        Token           = "token"
        Unrecognized    = "unrecognized"

    class GatewayRejectionReason(object):
        """
        Constants representing gateway rejection reasons. Available types are:

        * braintree.Transaction.GatewayRejectionReason.Avs
        * braintree.Transaction.GatewayRejectionReason.AvsAndCvv
        * braintree.Transaction.GatewayRejectionReason.Cvv
        * braintree.Transaction.GatewayRejectionReason.Duplicate
        """
        Avs          = "avs"
        AvsAndCvv    = "avs_and_cvv"
        Cvv          = "cvv"
        Duplicate    = "duplicate"
        Fraud        = "fraud"
        Unrecognized = "unrecognized"

    class Source(object):
        Api          = "api"
        ControlPanel = "control_panel"
        Recurring    = "recurring"
        Unrecognized = "unrecognized"

    class EscrowStatus(object):
        """
        Constants representing transaction escrow statuses. Available statuses are:

        * braintree.Transaction.EscrowStatus.HoldPending
        * braintree.Transaction.EscrowStatus.Held
        * braintree.Transaction.EscrowStatus.ReleasePending
        * braintree.Transaction.EscrowStatus.Released
        * braintree.Transaction.EscrowStatus.Refunded
        """

        HoldPending    = "hold_pending"
        Held           = "held"
        ReleasePending = "release_pending"
        Released       = "released"
        Refunded       = "refunded"
        Unrecognized   = "unrecognized"

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
        * braintree.Transaction.Status.Settling
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
        SettlementConfirmed    = "settlement_confirmed"
        SettlementDeclined     = "settlement_declined"
        SettlementFailed       = "settlement_failed"
        Settling               = "settling"
        SubmittedForSettlement = "submitted_for_settlement"
        Voided                 = "voided"
        Unrecognized           = "unrecognized"

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
    def cancel_release(transaction_id):
        """
        Cancels a pending release from escrow for a transaction.

        Requires the transaction id::

            result = braintree.Transaction.cancel_release("my_transaction_id")

        """

        return Configuration.gateway().transaction.cancel_release(transaction_id)

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
        Creates a transaction of type Credit.

        Amount is required. Also, a credit card,
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
    def hold_in_escrow(transaction_id):
        """
        Holds an existing submerchant transaction for escrow.

        It expects a transaction_id.::

            result = braintree.Transaction.hold_in_escrow("my_transaction_id")
        """
        return Configuration.gateway().transaction.hold_in_escrow(transaction_id)


    @staticmethod
    def refund(transaction_id, amount=None):
        """
        Refunds an existing transaction.

        It expects a transaction_id.::

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
    def release_from_escrow(transaction_id):
        """
        Submits an escrowed transaction for release.

        Requires the transaction id::

            result = braintree.Transaction.release_from_escrow("my_transaction_id")

        """

        return Configuration.gateway().transaction.release_from_escrow(transaction_id)

    @staticmethod
    def submit_for_settlement(transaction_id, amount=None):
        """
        Submits an authorized transaction for settlement.

        Requires the transaction id::

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
        Voids an existing transaction.

        It expects a transaction_id.::

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
        return ["amount", "channel", {"options": ["submit_for_settlement"]}]

    @staticmethod
    def create_signature():
        return [
            "amount", "customer_id", "device_session_id", "fraud_merchant_id", "merchant_account_id", "order_id", "channel",
            "payment_method_token", "purchase_order_number", "recurring", "shipping_address_id",
            "device_data", "billing_address_id", "payment_method_nonce", "tax_amount",
            "tax_exempt", "three_d_secure_token", "type", "venmo_sdk_payment_method_code", "service_fee_amount",
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
                    "add_billing_address_to_payment_method",
                    "hold_in_escrow",
                    "store_in_vault",
                    "store_in_vault_on_success",
                    "store_shipping_address_in_vault",
                    "submit_for_settlement",
                    "venmo_sdk_session"
                ]
            },
            {"custom_fields": ["__any_key__"]},
            {"descriptor": ["name", "phone", "url"]}
        ]

    def __init__(self, gateway, attributes):
        if "refund_id" in attributes:
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
        if "paypal" in attributes:
            self.paypal_details = PayPalAccount(gateway, attributes.pop("paypal"))
        if "sepa_bank_account" in attributes:
            self.sepa_bank_account_details = SEPABankAccount(gateway, attributes.pop("sepa_bank_account"))
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
        if "disbursement_details" in attributes:
            self.disbursement_details = DisbursementDetail(attributes.pop("disbursement_details"))
        if "disputes" in attributes:
            self.disputes = [Dispute(dispute) for dispute in self.disputes]
        if "payment_instrument_type" in attributes:
            self.payment_instrument_type = attributes["payment_instrument_type"]

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

    @property
    def is_disbursed(self):
       return self.disbursement_details.is_valid

