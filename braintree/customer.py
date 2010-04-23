from braintree.util.http import Http
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.resource import Resource
from braintree.credit_card import CreditCard
from braintree.address import Address
from braintree.configuration import Configuration
from braintree.exceptions.not_found_error import NotFoundError
from braintree.transparent_redirect import TransparentRedirect

class Customer(Resource):
    """
    A class representing a customer.

    An example of creating an customer with all available fields::

        result = braintree.Customer.create({
            "id": "my_customer_id",
            "company": "Some company",
            "email": "john.doe@example.com",
            "fax": "123-555-1212",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "123-555-1221",
            "website": "http://www.example.com",
            "credit_card": {
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
            },
            "custom_fields": {
                "my_key": "some value"
            }
        })

        print(result.customer.id)
        print(result.customer.first_name)

    For more information on Customers, see http://www.braintreepaymentsolutions.com/gateway/customer-api
    """

    @staticmethod
    def confirm_transparent_redirect(query_string):
        """
        Confirms a transparent redirect request.  It expects the query string from the
        redirect request.  The query string should _not_ include the leading "?" character. ::

            result = braintree.Customer.confirm_transparent_redirect_request("foo=bar&id=12345")
        """

        id = TransparentRedirect.parse_and_validate_query_string(query_string)
        return Customer.__post("/customers/all/confirm_transparent_redirect_request", {"id": id})

    @staticmethod
    def create(params={}):
        """
        Create a Customer::

            result = braintree.Customer.create({
                "company": "Some company",
                "first_name": "John"
            })
        """

        Resource.verify_keys(params, Customer.create_signature())
        return Customer.__post("/customers", {"customer": params})

    @staticmethod
    def delete(customer_id):
        """
        Delete a customer, given a customer_id::

            result = braintree.Customer.delete("my_customer_id")
        """

        Http().delete("/customers/" + customer_id)
        return SuccessfulResult()

    @staticmethod
    def find(customer_id):
        """
        Find an customer, given a customer_id.  This does not return a result
        object.  This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>` if the provided customer_id
        is not found. ::

            customer = braintree.Customer.find("my_customer_id")
        """

        try:
            response = Http().get("/customers/" + customer_id)
            return Customer(response["customer"])
        except NotFoundError:
            raise NotFoundError("customer with id " + customer_id + " not found")

    @staticmethod
    def tr_data_for_create(tr_data, redirect_url):
        """ Builds tr_data for creating a Customer. """

        Resource.verify_keys(tr_data, [{"customer": Customer.create_signature()}])
        return TransparentRedirect.tr_data(tr_data, redirect_url)

    @staticmethod
    def tr_data_for_update(tr_data, redirect_url):
        """ Builds tr_data for updating a Customer. """

        Resource.verify_keys(tr_data, [{"customer": Customer.update_signature()}])
        return TransparentRedirect.tr_data(tr_data, redirect_url)

    @staticmethod
    def transparent_redirect_create_url():
        """ Returns the url to use for creating Customers through transparent redirect. """

        return Configuration.base_merchant_url() + "/customers/all/create_via_transparent_redirect_request"

    @staticmethod
    def transparent_redirect_update_url():
        """ Returns the url to use for updating Customers through transparent redirect. """

        return Configuration.base_merchant_url() + "/customers/all/update_via_transparent_redirect_request"

    @staticmethod
    def update(customer_id, params={}):
        """
        Update an existing Customer by customer_id.  The params are similar to create::

            result = braintree.Customer.update("my_customer_id", {
                "last_name": "Smith"
            })
        """

        Resource.verify_keys(params, Customer.update_signature())
        response = Http().put("/customers/" + customer_id, {"customer": params})
        if "customer" in response:
            return SuccessfulResult({"customer": Customer(response["customer"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])

    @staticmethod
    def create_signature():
        return [
            "company", "email", "fax", "first_name", "id", "last_name", "phone", "website",
            {"credit_card": CreditCard.create_signature()},
            {"custom_fields": ["__any_key__"]}
        ]

    @staticmethod
    def update_signature():
        return [
            "company", "email", "fax", "first_name", "id", "last_name", "phone", "website",
            {"custom_fields": ["__any_key__"]}
        ]

    @staticmethod
    def __post(url, params={}):
        response = Http().post(url, params)
        if "customer" in response:
            return SuccessfulResult({"customer": Customer(response["customer"])})
        elif "api_error_response" in response:
            return ErrorResult(response["api_error_response"])
        else:
            pass

    def __init__(self, attributes):
        Resource.__init__(self, attributes)
        if "credit_cards" in attributes:
            self.credit_cards = [CreditCard(credit_card) for credit_card in self.credit_cards]
        if "addresses" in attributes:
            self.addresses = [Address(address) for address in self.addresses]
