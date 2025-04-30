import braintree
import warnings
from decimal import Decimal
from braintree.add_on import AddOn
from braintree.address import Address
from braintree.amex_express_checkout_card import AmexExpressCheckoutCard
from braintree.android_pay_card import AndroidPayCard
from braintree.apple_pay_card import ApplePayCard
from braintree.authorization_adjustment import AuthorizationAdjustment
from braintree.configuration import Configuration
from braintree.credit_card import CreditCard
from braintree.customer import Customer
from braintree.descriptor import Descriptor
from braintree.disbursement_detail import DisbursementDetail
from braintree.discount import Discount
from braintree.dispute import Dispute
from braintree.error_result import ErrorResult
from braintree.europe_bank_account import EuropeBankAccount
from braintree.exceptions.not_found_error import NotFoundError
from braintree.facilitated_details import FacilitatedDetails
from braintree.facilitator_details import FacilitatorDetails
from braintree.liability_shift import LiabilityShift
from braintree.local_payment import LocalPayment
from braintree.masterpass_card import MasterpassCard
from braintree.meta_checkout_card import MetaCheckoutCard
from braintree.meta_checkout_token import MetaCheckoutToken
from braintree.payment_facilitator import PaymentFacilitator
from braintree.payment_instrument_type import PaymentInstrumentType
from braintree.paypal_account import PayPalAccount
from braintree.paypal_here import PayPalHere
from braintree.resource import Resource
from braintree.resource_collection import ResourceCollection
from braintree.risk_data import RiskData
from braintree.samsung_pay_card import SamsungPayCard
from braintree.sepa_direct_debit_account import SepaDirectDebitAccount
from braintree.package_details import PackageDetails
from braintree.status_event import StatusEvent
from braintree.subscription_details import SubscriptionDetails
from braintree.successful_result import SuccessfulResult
from braintree.three_d_secure_info import ThreeDSecureInfo
from braintree.transaction_line_item import TransactionLineItem
from braintree.us_bank_account import UsBankAccount
from braintree.venmo_account import VenmoAccount
from braintree.visa_checkout_card import VisaCheckoutCard


class Transaction(Resource):
    """
    A class representing Braintree Transaction objects.

    An example of creating a sale transaction with all available fields::

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
                "company": "Braintree",
                "country_name": "United States of America",
                "extended_address": "Suite 403",
                "first_name": "Carl",
                "international_phone": { "country_code": "1", "national_number": "3121234567" },
                "last_name": "Jones",
                "locality": "Chicago",
                "phone_number": "312-123-4567",
                "postal_code": "60622",
                "region": "IL",
                "street_address": "123 E Main St"
            },
            "shipping": {
                "company": "Braintree",
                "country_name": "United States of America",
                "extended_address": "Apt 2F",
                "first_name": "Andrew",
                "international_phone": { "country_code": "1", "national_number": "3121234567" },
                "last_name": "Mason",
                "locality": "Bartlett",
                "phone_number": "312-123-4567",
                "postal_code": "60103",
                "region": "IL",
                "street_address": "456 W Main St"
            }
        })

        print(result.transaction.amount)
        print(result.transaction.order_id)

    For more information on Transactions, see https://developer.paypal.com/braintree/docs/reference/request/transaction/sale/python

    """

    def __repr__(self):
      detail_list = [
       "acquirer_reference_number",
       "additional_processor_response",
       "amount",
       "authorization_adjustments",
       "authorization_expires_at",
       "avs_error_response_code",
       "avs_postal_code_response_code",
       "avs_street_address_response_code",
       "channel",
       "created_at",
       "credit_card_details",
       "currency_iso_code",
       "customer_id",
       "cvv_response_code",
       "debit_network",
       "discount_amount",
       "disputes",
       "foreign_retailer",
       "gateway_rejection_reason",
       "graphql_id",
       "id",
       "installments",
       "liability_shift",
       "merchant_account_id",
       "merchant_advice_code",
       "merchant_advice_code_text",
       "network_response_code",
       "network_response_text",
       "network_transaction_id",
       "order_id",
       "packages",
       "payment_instrument_type",
       "payment_method_token",
       "plan_id",
       "processed_with_network_token",
       "processor_authorization_code",
       "processor_response_code",
       "processor_response_text",
       "processor_settlement_response_code",
       "processor_settlement_response_text",
       "purchase_order_number",
       "recurring",
       "refund_id",
       "refunded_transaction_id",
       "retried",
       "retried_transaction_id",
       "retrieval_reference_number",
       "retry_ids",
       "settlement_batch_id",
       "shipping_amount",
       "shipping_tax_amount",
       "ships_from_postal_code",
       "status",
       "status_history",
       "subscription_id",
       "tax_amount",
       "tax_exempt",
       "type",
       "updated_at",
       "voice_referral_number",
       ]

      return super(Transaction, self).__repr__(detail_list)

    # NEXT_MAJOR_VERSION this can be an enum! they were added as of python 3.4 and we support 3.5+
    class CreatedUsing(object):
        """
        Constants representing how the transaction was created.  Available types are:

        * braintree.Transaction.CreatedUsing.FullInformation
        * braintree.Transaction.CreatedUsing.Token
        """

        FullInformation = "full_information"
        Token           = "token"

    # NEXT_MAJOR_VERSION this can be an enum! they were added as of python 3.4 and we support 3.5+
    class GatewayRejectionReason(object):
        """
        Constants representing gateway rejection reasons. Available types are:

        * braintree.Transaction.GatewayRejectionReason.Avs
        * braintree.Transaction.GatewayRejectionReason.AvsAndCvv
        * braintree.Transaction.GatewayRejectionReason.Cvv
        * braintree.Transaction.GatewayRejectionReason.Duplicate
        * braintree.Transaction.GatewayRejectionReason.ExcessiveRetry
        * braintree.Transaction.GatewayRejectionReason.Fraud
        * braintree.Transaction.GatewayRejectionReason.RiskThreshold
        * braintree.Transaction.GatewayRejectionReason.ThreeDSecure
        * braintree.Transaction.GatewayRejectionReason.TokenIssuance
        """
        ApplicationIncomplete = "application_incomplete"
        Avs                   = "avs"
        AvsAndCvv             = "avs_and_cvv"
        Cvv                   = "cvv"
        Duplicate             = "duplicate"
        ExcessiveRetry        = "excessive_retry"
        Fraud                 = "fraud"
        RiskThreshold         = "risk_threshold"
        ThreeDSecure          = "three_d_secure"
        TokenIssuance         = "token_issuance"

    # NEXT_MAJOR_VERSION this can be an enum! they were added as of python 3.4 and we support 3.5+
    class ReasonCode(object):
        ANY_REASON_CODE = 'any_reason_code'

    # NEXT_MAJOR_VERSION this can be an enum! they were added as of python 3.4 and we support 3.5+
    class Source(object):
        Api          = "api"
        ControlPanel = "control_panel"
        Recurring    = "recurring"

    # NEXT_MAJOR_VERSION this can be an enum! they were added as of python 3.4 and we support 3.5+
    class Status(object):
        """
        Constants representing transaction statuses. Available statuses are:

        * braintree.Transaction.Status.AuthorizationExpired
        * braintree.Transaction.Status.Authorized
        * braintree.Transaction.Status.Authorizing
        * braintree.Transaction.Status.SettlementPending
        * braintree.Transaction.Status.SettlementDeclined
        * braintree.Transaction.Status.Failed
        * braintree.Transaction.Status.GatewayRejected
        * braintree.Transaction.Status.ProcessorDeclined
        * braintree.Transaction.Status.Settled
        * braintree.Transaction.Status.Settling
        * braintree.Transaction.Status.SubmittedForSettlement
        * braintree.Transaction.Status.Voided
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
        SettlementPending      = "settlement_pending"
        Settling               = "settling"
        SubmittedForSettlement = "submitted_for_settlement"
        Voided                 = "voided"

    # NEXT_MAJOR_VERSION this can be an enum! they were added as of python 3.4 and we support 3.5+
    class Type(object):
        """
        Constants representing transaction types. Available types are:

        * braintree.Transaction.Type.Credit
        * braintree.Transaction.Type.Sale
        """

        Credit = "credit"
        Sale = "sale"

    # NEXT_MAJOR_VERSION this can be an enum! they were added as of python 3.4 and we support 3.5+
    class IndustryType(object):
        Lodging = "lodging"
        TravelAndCruise = "travel_cruise"
        TravelAndFlight = "travel_flight"

    # NEXT_MAJOR_VERSION this can be an enum! they were added as of python 3.4 and we support 3.5+
    class AdditionalCharge(object):
        Restaurant = "restaurant"
        GiftShop = "gift_shop"
        MiniBar = "mini_bar"
        Telephone = "telephone"
        Laundry = "laundry"
        Other = "other"

    @staticmethod
    def adjust_authorization(transaction_id, amount):
        """
        adjust authorization for an existing transaction.

        It expects a `transaction_id` and `amount`, which is the new total authorization amount

        result = braintree.Transaction.adjust_authorization("my_transaction_id", "amount")

        """
        return Configuration.gateway().transaction.adjust_authorization(transaction_id, amount)

    @staticmethod
    def clone_transaction(transaction_id, params):
        return Configuration.gateway().transaction.clone_transaction(transaction_id, params)

    @staticmethod
    def credit(params=None):
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
        if params is None:
            params = {}
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
    def refund(transaction_id, amount_or_options=None):
        """
        Refunds an existing transaction.

        It expects a transaction_id.::

            result = braintree.Transaction.refund("my_transaction_id")

        """

        return Configuration.gateway().transaction.refund(transaction_id, amount_or_options)


    @staticmethod
    def sale(params=None):
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
        if params is None:
            params = {}
        if "recurring" in params.keys():
            warnings.warn("Use transaction_source parameter instead", DeprecationWarning)
        params["type"] = Transaction.Type.Sale
        return Transaction.create(params)

    @staticmethod
    def search(*query):
        return Configuration.gateway().transaction.search(*query)

    @staticmethod
    def submit_for_settlement(transaction_id, amount=None, params=None):
        """
        Submits an authorized transaction for settlement.

        Requires the transaction id::

            result = braintree.Transaction.submit_for_settlement("my_transaction_id")

        """
        if params is None:
            params = {}
        return Configuration.gateway().transaction.submit_for_settlement(transaction_id, amount, params)

    @staticmethod
    def update_details(transaction_id, params=None):
        """
        Updates existing details for transaction submitted_for_settlement.

        Requires the transaction id::

            result = braintree.Transaction.update_details("my_transaction_id", {
                "amount": "100.00",
                "order_id": "123",
                "descriptor": {
                    "name": "123*123456789012345678",
                    "phone": "3334445555",
                    "url": "url.com"
                }
            )

        """
        if params is None:
            params = {}
        return Configuration.gateway().transaction.update_details(transaction_id, params)

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
            "amount",
            # NEXT_MAJOR_VERSION use google_pay_card in public API (map to android_pay_card internally)
            {"android_pay_card": ["number", "cryptogram", "expiration_month", "expiration_year", "eci_indicator", "source_card_type", "source_card_last_four", "google_transaction_id"]},
            {"apple_pay_card": ["number", "cardholder_name", "cryptogram", "expiration_month", "expiration_year", "eci_indicator"]},
            {
                "billing": [
                    "company", "country_code_alpha2", "country_code_alpha3",
                    "country_code_numeric", "country_name", "extended_address", "first_name",
                    {"international_phone": ["country_code", "national_number"]},
                    "last_name", "locality", "phone_number",
                    "postal_code", "region", "street_address"
                ]
            },
            "billing_address_id",
            {
                "credit_card": [
                    "cardholder_name", "cvv", "expiration_date", "expiration_month", "expiration_year",
                    {"network_tokenization_attributes": ["cryptogram", "ecommerce_indicator", "token_requestor_id"]},
                    "number",
                    {"payment_reader_card_details": ["encrypted_card_data", "key_serial_number"]},
                    "token"
                ]
            },
            {
                "customer": [
                    "id", "company", "email", "fax", "first_name", "last_name", "phone", "website"
                ]
            },
            "customer_id",
            {"custom_fields": ["__any_key__"]},
            "channel",
            {"descriptor": ["name", "phone", "url"]},
            "device_data",
            "device_session_id", # NEXT_MAJOR_VERSION remove device_session_id
            "discount_amount",
            "exchange_rate_quote_id",
            {"external_vault": ["status", "previous_network_transaction_id"]},
            "foreign_retailer",
            "fraud_merchant_id", # NEXT_MAJOR_VERSION remove fraud_merchant_id
            {"industry":
                [
                    "industry_type",
                    {
                        "data": [
                            "folio_number", "check_in_date", "check_out_date", "departure_date", "lodging_check_in_date", "lodging_check_out_date", "travel_package", "lodging_name", "room_rate",
                            "passenger_first_name", "passenger_last_name", "passenger_middle_initial", "passenger_title", "issued_date", "travel_agency_name", "travel_agency_code", "ticket_number",
                            "issuing_carrier_code", "customer_code", "fare_amount", "fee_amount", "room_tax", "tax_amount", "restricted_ticket", "no_show", "advanced_deposit", "fire_safe", "property_phone", "arrival_date", "ticket_issuer_address", "date_of_birth", "country_code",
                            {
                                "legs": [
                                    "conjunction_ticket", "exchange_ticket", "coupon_number", "service_class", "carrier_code", "fare_basis_code", "flight_number", "departure_date", "departure_airport_code", "departure_time",
                                    "arrival_airport_code", "arrival_time", "stopover_permitted", "fare_amount", "fee_amount", "tax_amount", "endorsement_or_restrictions"
                                ]
                            },
                            {
                                "additional_charges": [
                                  "kind", "amount"
                                ],
                            }
                        ]
                    }
                ]
            }, 
            {"installments": {"count"}},
            {"line_items":
                [
                    "commodity_code", "description", "discount_amount", "image_url", "kind", "name", "product_code", "quantity", "tax_amount", "total_amount", "unit_amount", "unit_of_measure", "unit_tax_amount", "upc_code", "upc_type", "url",
                ]
            },
            "merchant_account_id",
            {
                "options": [
                    "add_billing_address_to_payment_method",
                    "payee_id",
                    "payee_email",
                    "skip_advanced_fraud_checking",
                    "skip_avs",
                    "skip_cvv",
                    "store_in_vault",
                    "store_in_vault_on_success",
                    "store_shipping_address_in_vault",
                    "submit_for_settlement",
                    "venmo_sdk_session", # NEXT_MJOR_VERSION remove venmo_sdk_session
                    {
                        "credit_card": [
                            "account_type",
                            "process_debit_as_credit"
                        ],
                        "paypal": [
                            "custom_field",
                            "description", 
                            "payee_id",
                            "payee_email",
                            "recipient_email",
                            {"recipient_phone":["country_code", "national_number"]},
                            {"supplementary_data": ["__any_key__"]}
                        ],
                        "three_d_secure": [
                            "required"
                        ],
                        "amex_rewards": [
                            "request_id",
                            "points",
                            "currency_amount",
                            "currency_iso_code"
                        ],
                        "venmo_merchant_data": [
                            "venmo_merchant_public_id",
                            "originating_transaction_id",
                            "originating_merchant_id",
                            "originating_merchant_kind"
                        ],
                        "venmo": [
                            "profile_id"
                        ],
                    },
                    {
                        "adyen": [
                            "overwrite_brand",
                            "selected_brand"
                        ]
                    },
                    {
                        "processing_overrides": [
                            "customer_email",
                            "customer_first_name",
                            "customer_last_name",
                            "customer_tax_identifier"
                        ]
                    }
                ]
            },
            "order_id",
            "payment_method_nonce", "payment_method_token", "product_sku", "purchase_order_number",
            {"paypal_account": ["payee_id", "payee_email", "payer_id", "payment_id"]},
            "recurring",
            {
                "risk_data": [
                    "customer_browser", "customer_device_id", "customer_ip", "customer_location_zip", "customer_tenure"
                ]
            },
            "sca_exemption",
            "shared_customer_id", "shared_billing_address_id", "shared_payment_method_nonce", "shared_payment_method_token", "shared_shipping_address_id",
            {
                "shipping": [
                    "company", "country_code_alpha2", "country_code_alpha3",
                    "country_code_numeric", "country_name", "extended_address", "first_name",
                    {"international_phone": ["country_code", "national_number"]},
                    "last_name", "locality", "phone_number",
                    "postal_code", "region", "shipping_method", "street_address"
                ]
            },
            "shipping_address_id",
            "shipping_amount", "shipping_tax_amount", "ships_from_postal_code",
            "tax_amount",
            "tax_exempt", "three_d_secure_authentication_id",
            {
                "three_d_secure_pass_thru": [
                    "eci_flag",
                    "cavv",
                    "xid",
                    "authentication_response",
                    "directory_response",
                    "cavv_algorithm",
                    "ds_transaction_id",
                    "three_d_secure_version"
                ]
            },
            "three_d_secure_token", # NEXT_MAJOR_VERSION Remove three_d_secure_token
            {
                "payment_facilitator":[
                    "payment_facilitator_id",
                    {
                        "sub_merchant":[
                            "reference_number",
                            "tax_id",
                            "legal_name",
                            {
                                "address": [
                                    "street_address", "locality", "region", "country_code_alpha2", "postal_code",
                                    {"international_phone": ["country_code", "national_number"]}
                                ]
                            }

                        ]
                    }
                ]
            },
            "transaction_source",
            "type", "venmo_sdk_payment_method_code",  # NEXT_MJOR_VERSION remove venmo_sdk_payment_method_code
        ]

    @staticmethod
    def submit_for_settlement_signature():
        return [
                "order_id",
                {"descriptor": ["name", "phone", "url"]},
                "purchase_order_number",
                "tax_amount",
                "tax_exempt",
                "discount_amount",
                "shipping_amount",
                "shipping_tax_amount",
                "ships_from_postal_code",
                {"industry":
                    [
                        "industry_type",
                        {
                            "data": [
                                "advanced_deposit", "arrival_date", "check_in_date", "check_out_date", "customer_code", "departure_date", "fare_amount", "fee_amount", "fire_safe", "folio_number", "issued_date",  "issuing_carrier_code",
                                "lodging_check_in_date", "lodging_check_out_date", "lodging_name", "no_show", "passenger_first_name", "passenger_last_name", "passenger_middle_initial", "passenger_title", "property_phone",
                                "restricted_ticket", "room_rate",  "room_tax", "tax_amount", "ticket_issuer_address", "ticket_number", "travel_agency_code", "travel_agency_name", "travel_package",
                                {
                                    "legs": [
                                        "arrival_airport_code", "arrival_time", "carrier_code", "conjunction_ticket", "coupon_number", "departure_airport_code", "departure_date", "departure_time", "endorsement_or_restrictions",
                                        "exchange_ticket", "fare_amount", "fare_basis_code", "fee_amount",  "flight_number", "service_class", "stopover_permitted", "tax_amount"
                                    ]
                                },
                                {
                                    "additional_charges": [
                                      "amount", "kind"
                                    ],
                                }
                            ]
                        }
                    ]
                },
                {"line_items":
                    [
                        "commodity_code", "description", "discount_amount", "image_url", "kind", "name", "product_code", "quantity", "tax_amount", "total_amount", "unit_amount", "unit_of_measure", "unit_tax_amount", "upc_code", "upc_type", "url,"
                    ]
                },
                {"shipping":
                    [
                        "first_name", "last_name", "company", "country_code_alpha2", "country_code_alpha3",
                        "country_code_numeric", "country_name", "extended_address", "locality",
                        "postal_code", "region", "street_address",
                    ]
                },
                {"industry":
                    [
                        "industry_type",
                        {
                            "data": [
                                "folio_number", "check_in_date", "check_out_date", "departure_date", "lodging_check_in_date", "lodging_check_out_date", "travel_package", "lodging_name", "room_rate",
                                "passenger_first_name", "passenger_last_name", "passenger_middle_initial", "passenger_title", "issued_date", "travel_agency_name", "travel_agency_code", "ticket_number",
                                "issuing_carrier_code", "customer_code", "fare_amount", "fee_amount", "room_tax", "tax_amount", "restricted_ticket", "no_show", "advanced_deposit", "fire_safe", "property_phone", "arrival_date", "ticket_issuer_address", "date_of_birth", "country_code",
                                {
                                    "legs": [
                                        "conjunction_ticket", "exchange_ticket", "coupon_number", "service_class", "carrier_code", "fare_basis_code", "flight_number", "departure_date", "departure_airport_code", "departure_time",
                                        "arrival_airport_code", "arrival_time", "stopover_permitted", "fare_amount", "fee_amount", "tax_amount", "endorsement_or_restrictions"
                                    ]
                                },
                                {
                                    "additional_charges": [
                                        "kind", "amount"
                                    ],
                                }
                            ]
                        }
                    ]
                },
            ]

    @staticmethod
    def submit_for_partial_settlement_signature():
        return Transaction.submit_for_settlement_signature() + [
            "final_capture"
        ]

    @staticmethod
    def package_tracking_signature():
        return [ "carrier", "notify_payer", "tracking_number",
                { "line_items": [
                    "commodity_code", "description", "discount_amount", "image_url", "kind", "name",
                    "product_code", "quantity", "tax_amount", "total_amount", "unit_amount", "unit_of_measure",
                    "unit_tax_amount", "upc_code", "upc_type", "url"
                    ]
                },
            ]

    @staticmethod
    def package_tracking(transaction_id, params=None):
        """
        Creates a request to send package tracking information for a transaction which has already submitted for settlement.

        Requires the transaction id of the transaction and the package tracking request details::

            result = braintree.Transaction.package_tracking("my_transaction_id", params )

        """
        if params is None:
            params = {}
        return Configuration.gateway().transaction.package_tracking(transaction_id, params)


    @staticmethod
    def update_details_signature():
        return ["amount", "order_id", {"descriptor": ["name", "phone", "url"]}]

    @staticmethod
    def refund_signature():
        return ["amount", "order_id", "merchant_account_id"]

    @staticmethod
    def submit_for_partial_settlement(transaction_id, amount, params=None):
        """
        Creates a partial settlement transaction for an authorized transaction

        Requires the transaction id of the authorized transaction and an amount::

            result = braintree.Transaction.submit_for_partial_settlement("my_transaction_id", "20.00")

        """
        if params is None:
            params = {}
        return Configuration.gateway().transaction.submit_for_partial_settlement(transaction_id, amount, params)

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)

        self.amount = Decimal(self.amount)
        if "tax_amount" in attributes and getattr(self, "tax_amount", None):
            self.tax_amount = Decimal(self.tax_amount)
        if "discount_amount" in attributes and getattr(self, "discount_amount", None):
            self.discount_amount = Decimal(self.discount_amount)
        if "shipping_amount" in attributes and getattr(self, "shipping_amount", None):
            self.shipping_amount = Decimal(self.shipping_amount)
        if "shipping_tax_amount" in attributes and getattr(self, "shipping_tax_amount", None):
            self.shipping_tax_amount = Decimal(self.shipping_tax_amount)
        if "billing" in attributes:
            self.billing_details = Address(gateway, attributes.pop("billing"))
        if "credit_card" in attributes:
            self.credit_card_details = CreditCard(gateway, attributes.pop("credit_card"))
        if "shipments" in attributes:
            self.packages = [PackageDetails(detail) for detail in self.shipments]
        if "paypal" in attributes:
            self.paypal_details = PayPalAccount(gateway, attributes.pop("paypal"))
        if "paypal_here" in attributes:
            self.paypal_here_details = PayPalHere(gateway, attributes.pop("paypal_here"))
        if "local_payment" in attributes:
            self.local_payment_details = LocalPayment(gateway, attributes.pop("local_payment"))
        if "sepa_debit_account_detail" in attributes:
            self.sepa_direct_debit_account_details = SepaDirectDebitAccount(gateway, attributes.pop("sepa_debit_account_detail"))
        if "europe_bank_account" in attributes:
            self.europe_bank_account_details = EuropeBankAccount(gateway, attributes.pop("europe_bank_account"))
        if "us_bank_account" in attributes:
            self.us_bank_account = UsBankAccount(gateway, attributes.pop("us_bank_account"))
        if "apple_pay" in attributes:
            self.apple_pay_details = ApplePayCard(gateway, attributes.pop("apple_pay"))
        # NEXT_MAJOR_VERSION rename to google_pay_card_details
        if "android_pay_card" in attributes:
            self.android_pay_card_details = AndroidPayCard(gateway, attributes.pop("android_pay_card"))
        # NEXT_MAJOR_VERSION remove amex express checkout
        if "amex_express_checkout_card" in attributes:
            self.amex_express_checkout_card_details = AmexExpressCheckoutCard(gateway, attributes.pop("amex_express_checkout_card"))
        if "venmo_account" in attributes:
            self.venmo_account_details = VenmoAccount(gateway, attributes.pop("venmo_account"))
        if "visa_checkout_card" in attributes:
            self.visa_checkout_card_details = VisaCheckoutCard(gateway, attributes.pop("visa_checkout_card"))
        # NEXT_MAJOR_VERSION remove masterpass
        if "masterpass_card" in attributes:
            self.masterpass_card_details = MasterpassCard(gateway, attributes.pop("masterpass_card"))
        # NEXT_MAJOR_VERSION remove SamsungPayCard
        if "samsung_pay_card" in attributes:
            self.samsung_pay_card_details = SamsungPayCard(gateway, attributes.pop("samsung_pay_card"))
        if "meta_checkout_card" in attributes:
            self.meta_checkout_card_details = MetaCheckoutCard(gateway, attributes.pop("meta_checkout_card"))
        if "meta_checkout_token" in attributes:
            self.meta_checkout_token_details = MetaCheckoutToken(gateway, attributes.pop("meta_checkout_token"))
        if "sca_exemption_requested" in attributes:
            self.sca_exemption_requested = attributes.pop("sca_exemption_requested")
        else:
            self.sca_exemption_requested = None
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
        if "authorization_adjustments" in attributes:
            self.authorization_adjustments = [AuthorizationAdjustment(authorization_adjustment) for authorization_adjustment in self.authorization_adjustments]
        if "payment_instrument_type" in attributes:
            self.payment_instrument_type = attributes["payment_instrument_type"]
        if "risk_data" in attributes:
            self.risk_data = RiskData(attributes["risk_data"])
        else:
            self.risk_data = None
        if "three_d_secure_info" in attributes and not attributes["three_d_secure_info"] is None:
            self.three_d_secure_info = ThreeDSecureInfo(attributes["three_d_secure_info"])
        else:
            self.three_d_secure_info = None
        if "facilitated_details" in attributes:
            self.facilitated_details = FacilitatedDetails(attributes.pop("facilitated_details"))
        if "facilitator_details" in attributes:
            self.facilitator_details = FacilitatorDetails(attributes.pop("facilitator_details"))
        if "network_transaction_id" in attributes:
            self.network_transaction_id = attributes["network_transaction_id"]
        if "payment_facilitator" in attributes:
            self.payment_facilitator = PaymentFacilitator(attributes.pop("payment_facilitator"))

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

    @property
    def line_items(self):
        """
        The line items associated with this transaction
        """
        return self.gateway.transaction_line_item.find_all(self.id)
