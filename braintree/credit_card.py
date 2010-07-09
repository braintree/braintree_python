import braintree
import warnings
from braintree.util.http import Http
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.resource import Resource
from braintree.address import Address
from braintree.exceptions.not_found_error import NotFoundError
from braintree.configuration import Configuration
from braintree.ids_search import IdsSearch
from braintree.resource_collection import ResourceCollection
from braintree.transparent_redirect import TransparentRedirect

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
            },
            "options": {
                "verify_card": True
            }
        })

        print(result.credit_card.token)
        print(result.credit_card.masked_number)

    For more information on CreditCards, see http://www.braintreepaymentsolutions.com/gateway/credit-card-api

    For more information on CreditCard verifications, see http://www.braintreepaymentsolutions.com/gateway/credit-card-verification-api
    """
    class CardType(object):
        """
        Contants representing the type of the credit card.  Available types are:

        * Braintree.CreditCard.AmEx
        * Braintree.CreditCard.CarteBlanche
        * Braintree.CreditCard.ChinaUnionPay
        * Braintree.CreditCard.DinersClubInternational
        * Braintree.CreditCard.Discover
        * Braintree.CreditCard.JCB
        * Braintree.CreditCard.Laser
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
        JCB = "JCB"
        Laser = "Laser"
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

    @staticmethod
    def confirm_transparent_redirect(query_string):
        """
        Confirms a transparent redirect request. It expects the query string from the
        redirect request. The query string should _not_ include the leading "?" character. ::

            result = braintree.CreditCard.confirm_transparent_redirect_request("foo=bar&id=12345")
        """

        warnings.warn("Please use TransparentRedirect.confirm instead", DeprecationWarning)
        id = TransparentRedirect.parse_and_validate_query_string(query_string)["id"][0]
        return CreditCard._post("/payment_methods/all/confirm_transparent_redirect_request", {"id": id})

    @staticmethod
    def create(params={}):
        """
        Create an CreditCard.  A number and expiration_date are required. ::

            result = braintree.CreditCard.create({
                "number": "4111111111111111",
                "expiration_date": "12/2012"
            })
        """

        Resource.verify_keys(params, CreditCard.create_signature())
        return CreditCard._post("/payment_methods", {"credit_card": params})

    @staticmethod
    def update(credit_card_token, params={}):
        """
        Update an existing CreditCard by credit_card_id.  The params are similar to create::

            result = braintree.CreditCard.update("my_credit_card_id", {
                "cardholder_name": "John Doe"
            })
        """

        Resource.verify_keys(params, CreditCard.update_signature())
        response = Http().put("/payment_methods/" + credit_card_token, {"credit_card": params})
        if "credit_card" in response:
            return SuccessfulResult({"credit_card": CreditCard(response["credit_card"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    @staticmethod
    def delete(credit_card_token):
        """
        Delete a credit card, given a credit_card_id::

            result = braintree.CreditCard.delete("my_credit_card_id")
        """

        Http().delete("/payment_methods/" + credit_card_token)
        return SuccessfulResult()

    @staticmethod
    def expired():
        """ Return a collection of expired credit cards. """
        response = Http().post("/payment_methods/all/expired_ids")
        return ResourceCollection(None, response, CreditCard.__fetch_expired)

    @staticmethod
    def expiring_between(start_date, end_date):
        """ Return a collection of credit cards expiring between the given dates. """
        formatted_start_date = start_date.strftime("%m%Y")
        formatted_end_date = end_date.strftime("%m%Y")
        query = "start=%s&end=%s" % (formatted_start_date, formatted_end_date)
        response = Http().post("/payment_methods/all/expiring_ids?" + query)
        return ResourceCollection(query, response, CreditCard.__fetch_existing_between)

    @staticmethod
    def __fetch_expired(query, ids):
        criteria = {}
        criteria["ids"] = IdsSearch.ids.in_list(ids).to_param()
        response = Http().post("/payment_methods/all/expired", {"search": criteria})
        return [CreditCard(item) for item in ResourceCollection._extract_as_array(response["payment_methods"], "credit_card")]

    @staticmethod
    def __fetch_existing_between(query, ids):
        criteria = {}
        criteria["ids"] = IdsSearch.ids.in_list(ids).to_param()
        response = Http().post("/payment_methods/all/expiring?" + query, {"search": criteria})
        return [CreditCard(item) for item in ResourceCollection._extract_as_array(response["payment_methods"], "credit_card")]

    @staticmethod
    def find(credit_card_token):
        """
        Find a credit card, given a credit_card_id. This does not return
        a result object. This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>` if the provided
        credit_card_id is not found. ::

            credit_card = braintree.CreditCard.find("my_credit_card_id")
        """

        try:
            response = Http().get("/payment_methods/" + credit_card_token)
            return CreditCard(response["credit_card"])
        except NotFoundError:
            raise NotFoundError("payment method with token " + credit_card_token + " not found")

    @staticmethod
    def create_signature():
        return CreditCard.signature("create")

    @staticmethod
    def update_signature():
        return CreditCard.signature("update")

    @staticmethod
    def signature(type):
        billing_address_params = [
            "company", "country_code_alpha2", "country_code_alpha3", "country_code_numeric", "country_name",
            "extended_address", "first_name", "last_name", "locality", "postal_code", "region", "street_address"
        ]
        options = ["make_default", "verification_merchant_account_id", "verify_card"]

        signature = [
            "cardholder_name", "cvv", "expiration_date", "expiration_month", "expiration_year", "number", "token",
            {"billing_address": billing_address_params},
            {"options": options}
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

    @staticmethod
    def transparent_redirect_create_url():
        """
        Returns the url to use for creating CreditCards through transparent redirect.
        """
        warnings.warn("Please use TransparentRedirect.url instead", DeprecationWarning)
        return Configuration.base_merchant_url() + "/payment_methods/all/create_via_transparent_redirect_request"

    @staticmethod
    def tr_data_for_create(tr_data, redirect_url):
        """
        Builds tr_data for CreditCard creation.
        """

        Resource.verify_keys(tr_data, [{"credit_card": CreditCard.create_signature()}])
        tr_data["kind"] = TransparentRedirect.Kind.CreatePaymentMethod
        return TransparentRedirect.tr_data(tr_data, redirect_url)

    @staticmethod
    def tr_data_for_update(tr_data, redirect_url):
        """
        Builds tr_data for CreditCard updating.
        """
        Resource.verify_keys(tr_data, ["payment_method_token", {"credit_card": CreditCard.update_signature()}])
        tr_data["kind"] = TransparentRedirect.Kind.UpdatePaymentMethod
        return TransparentRedirect.tr_data(tr_data, redirect_url)

    @staticmethod
    def transparent_redirect_update_url():
        """
        Returns the url to be used for updating CreditCards through transparent redirect.
        """
        warnings.warn("Please use TransparentRedirect.url instead", DeprecationWarning)
        return Configuration.base_merchant_url() + "/payment_methods/all/update_via_transparent_redirect_request"

    @staticmethod
    def _post(url, params={}):
        response = Http().post(url, params)
        if "credit_card" in response:
            return SuccessfulResult({"credit_card": CreditCard(response["credit_card"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    def __init__(self, attributes):
        Resource.__init__(self, attributes)
        self.is_expired = self.expired
        if "billing_address" in attributes:
            self.billing_address = Address(self.billing_address)
        else:
            self.billing_address = None

        if "subscriptions" in attributes:
            self.subscriptions = [braintree.subscription.Subscription(subscription) for subscription in self.subscriptions]

    @property
    def expiration_date(self):
        return self.expiration_month + "/" + self.expiration_year

    @property
    def masked_number(self):
        """
        Returns the masked number of the CreditCard.
        """
        return self.bin + "******" + self.last_4

