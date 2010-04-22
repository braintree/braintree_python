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
from braintree.resource_collection import ResourceCollection
from braintree.transparent_redirect import TransparentRedirect
from braintree.exceptions.not_found_error import NotFoundError

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
                "website": "http://braintreepaymentsolutions.com"
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

    For more information on Transactions, see http://www.braintreepaymentsolutions.com/gateway/transaction-api
    """

    class Type(object):
        """
        Constants representing transaction types. Available types are:

        * braintree.Transaction.Type.Sale
        * braintree.Transaction.Type.Credit
        """

        Sale = "sale"
        Credit = "credit"

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
        * braintree.Transaction.Status.Unknown
        * braintree.Transaction.Status.Unrecognized
        * braintree.Transaction.Status.Void
        """

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
        """
        Confirms a transparent redirect request. It expects the query string from the
        redirect request. The query string should _not_ include the leading "?" character. ::

            result = braintree.Transaction.confirm_transparent_redirect_request("foo=bar&id=12345")
        """

        id = TransparentRedirect.parse_and_validate_query_string(query_string)
        return Transaction.__post("/transactions/all/confirm_transparent_redirect_request", {"id": id})

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

        try:
            response = Http().get("/transactions/" + transaction_id)
            return Transaction(response["transaction"])
        except NotFoundError:
            raise NotFoundError("transaction with id " + transaction_id + " not found")

    @staticmethod
    def refund(transaction_id):
        """
        Refunds an existing transaction. It expects a transaction_id. ::

            result = braintree.Transaction.refund("my_transaction_id")
        """

        response = Http().post("/transactions/" + transaction_id + "/refund", {})
        if "transaction" in response:
            return SuccessfulResult({"transaction": Transaction(response["transaction"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])


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
    def search(query, page=1):
        """
        Search for transactions based on keywords. For example, you can search for
        transactions based on the credit card bin. The search will return a
        :class:`ResourceCollection <braintree.resource_collection.ResourceCollection>`::

            collection = braintree.Transaction.search("411111")

            for transaction in collection:
                pass

            next_page = collection.next_page()

            for transaction in next_page:
                pass
        """

        query_string = urllib.urlencode([("q", query), ("page", page)])
        response = Http().get("/transactions/all/search?" + query_string)
        return ResourceCollection(query, response["credit_card_transactions"], Transaction)

    @staticmethod
    def submit_for_settlement(transaction_id, amount=None):
        """
        Submits an authorized transaction for settlement. ::

            result = braintree.Transaction.submit_for_settlement("my_transaction_id")
        """

        response = Http().put("/transactions/" + transaction_id + "/submit_for_settlement",
                {"transaction": {"amount": amount}})
        if "transaction" in response:
            return SuccessfulResult({"transaction": Transaction(response["transaction"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    @staticmethod
    def tr_data_for_credit(tr_data, redirect_url):
        """
        Builds tr_data for a Transaction of type Credit
        """

        if "transaction" not in tr_data:
            tr_data["transaction"] = {}
        tr_data["transaction"]["type"] = Transaction.Type.Credit
        Resource.verify_keys(tr_data, [{"transaction": Transaction.create_signature()}])
        return TransparentRedirect.tr_data(tr_data, redirect_url)

    @staticmethod
    def tr_data_for_sale(tr_data, redirect_url):
        """
        Builds tr_data for a Transaction of type Credit
        """

        if "transaction" not in tr_data:
            tr_data["transaction"] = {}
        tr_data["transaction"]["type"] = Transaction.Type.Sale
        Resource.verify_keys(tr_data, [{"transaction": Transaction.create_signature()}])
        return TransparentRedirect.tr_data(tr_data, redirect_url)

    @staticmethod
    def transparent_redirect_create_url():
        """
        Returns the url to be used for creating Transactions through transparent redirect.
        """

        return Configuration.base_merchant_url() + "/transactions/all/create_via_transparent_redirect_request"

    @staticmethod
    def void(transaction_id):
        """
        Voids an existing transaction. It expects a transaction_id. ::

            result = braintree.Transaction.void("my_transaction_id")
        """

        response = Http().put("/transactions/" + transaction_id + "/void")
        if "transaction" in response:
            return SuccessfulResult({"transaction": Transaction(response["transaction"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

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

        Resource.verify_keys(params, Transaction.create_signature())
        return Transaction.__post("/transactions", {"transaction": params})

    @staticmethod
    def create_signature():
        return [
            "amount", "customer_id", "order_id", "payment_method_token", "type",
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
        """
        The vault billing address associated with this transaction
        """

        return Address.find(self.customer_details.id, self.billing_details.id)

    @property
    def vault_credit_card(self):
        """
        The vault credit card associated with this transaction
        """

        return CreditCard.find(self.credit_card_details.token)

    @property
    def vault_customer(self):
        """
        The vault customer associated with this transaction
        """

        return Customer.find(self.customer_details.id)
