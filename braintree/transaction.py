import urllib
from decimal import Decimal
from braintree.util.http import Http
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.resource import Resource
from braintree.address import Address
from braintree.configuration import Configuration
from braintree.credit_card import CreditCard
from braintree.customer import Customer
from braintree.paged_collection import PagedCollection
from braintree.transparent_redirect import TransparentRedirect
from braintree.exceptions.not_found_error import NotFoundError

class Transaction(Resource):
    class Type(object):
        Sale = "sale"
        Credit = "credit"

    class Status(object):
        Authorized             = "authorized"
        Authorizing            = "authorizing"
        Failed                 = "failed"
        GatewayRejected        = "gateway_rejected"
        ProcessorDeclined      = "processor_declined"
        Settled                = "settled"
        SettlementFailed       = "settlement_failed"
        SubmittedForSettlement = "submitted_for_settlement"
        Unknown                = "unknown"
        Unrecognized           = "unrecognized"
        Voided                 = "voided"

    @staticmethod
    def confirm_transparent_redirect(query_string):
        id = TransparentRedirect.parse_and_validate_query_string(query_string)
        return Transaction.__post("/transactions/all/confirm_transparent_redirect_request", {"id": id})

    @staticmethod
    def credit(params={}):
        params["type"] = Transaction.Type.Credit
        return Transaction.create(params)

    @staticmethod
    def find(transaction_id):
        try:
            response = Http().get("/transactions/" + transaction_id)
            return Transaction(response["transaction"])
        except NotFoundError:
            raise NotFoundError("transaction with id " + transaction_id + " not found")

    @staticmethod
    def refund(transaction_id):
        response = Http().post("/transactions/" + transaction_id + "/refund", {})
        if "transaction" in response:
            return SuccessfulResult({"transaction": Transaction(response["transaction"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])


    @staticmethod
    def sale(params={}):
        params["type"] = Transaction.Type.Sale
        return Transaction.create(params)

    @staticmethod
    def search(query, page=1):
        query_string = urllib.urlencode([("q", query), ("page", page)])
        response = Http().get("/transactions/all/search?" + query_string)
        return PagedCollection(query, response["credit_card_transactions"], Transaction)

    @staticmethod
    def submit_for_settlement(transaction_id, amount=None):
        response = Http().put("/transactions/" + transaction_id + "/submit_for_settlement",
                {"transaction": {"amount": amount}})
        if "transaction" in response:
            return SuccessfulResult({"transaction": Transaction(response["transaction"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    @staticmethod
    def tr_data_for_credit(tr_data, redirect_url):
        if "transaction" not in tr_data:
            tr_data["transaction"] = {}
        tr_data["transaction"]["type"] = Transaction.Type.Credit
        Resource.verify_keys(tr_data, [{"transaction": Transaction.create_signature()}])
        return TransparentRedirect.tr_data(tr_data, redirect_url)

    @staticmethod
    def tr_data_for_sale(tr_data, redirect_url):
        if "transaction" not in tr_data:
            tr_data["transaction"] = {}
        tr_data["transaction"]["type"] = Transaction.Type.Sale
        Resource.verify_keys(tr_data, [{"transaction": Transaction.create_signature()}])
        return TransparentRedirect.tr_data(tr_data, redirect_url)

    @staticmethod
    def transparent_redirect_create_url():
        return Configuration.base_merchant_url() + "/transactions/all/create_via_transparent_redirect_request"

    @staticmethod
    def void(transaction_id):
        response = Http().put("/transactions/" + transaction_id + "/void")
        if "transaction" in response:
            return SuccessfulResult({"transaction": Transaction(response["transaction"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    @staticmethod
    def create(params):
        Resource.verify_keys(params, Transaction.create_signature())
        return Transaction.__post("/transactions", {"transaction": params})

    @staticmethod
    def create_signature():
        return [
            "amount", "customer_id", "order_id", "payment_method_token", "type",
            {
                "credit_card": [
                    "token", "cvv", "expiration_date", "number"
                ]
            },
            {
                "customer": [
                    "id", "company", "email", "fax", "first_name", "last_name", "phone", "website"
                ]
            },
            {
                "billing": [
                    "first_name", "last_name", "company", "country_name", "extended_address", "locality",
                    "postal_code", "region", "street_address"
                ]
            },
            {
                "shipping": [
                    "first_name", "last_name", "company", "country_name", "extended_address", "locality",
                    "postal_code", "region", "street_address"
                ]
            },
            {
                "options": [
                    "store_in_vault", "submit_for_settlement", "add_billing_address_to_payment_method",
                    "store_shipping_address_in_vault"
                ]
            },
            {"custom_fields": ["__any_key__"]}
        ]

    @staticmethod
    def __post(url, params):
        response = Http().post(url, params)
        if "transaction" in response:
            return SuccessfulResult({"transaction": Transaction(response["transaction"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    def __init__(self, attributes):
        if "billing" in attributes:
            attributes["billing_details"] = Address(attributes.pop("billing"))
        if "credit_card" in attributes:
            attributes["credit_card_details"] = CreditCard(attributes.pop("credit_card"))
        if "customer" in attributes:
            attributes["customer_details"] = Customer(attributes.pop("customer"))
        if "shipping" in attributes:
            attributes["shipping_details"] = Address(attributes.pop("shipping"))
        Resource.__init__(self, attributes)
        self.amount = Decimal(self.amount)

    @property
    def vault_billing_address(self):
        return Address.find(self.customer_details.id, self.billing_details.id)

    @property
    def vault_credit_card(self):
        return CreditCard.find(self.credit_card_details.token)

    @property
    def vault_customer(self):
        return Customer.find(self.customer_details.id)
