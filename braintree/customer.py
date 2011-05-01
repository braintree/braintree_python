import warnings
from braintree.util.http import Http
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.resource import Resource
from braintree.credit_card import CreditCard
from braintree.address import Address
from braintree.configuration import Configuration
from braintree.ids_search import IdsSearch
from braintree.exceptions.not_found_error import NotFoundError
from braintree.resource_collection import ResourceCollection
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

    For more information on Customers, see http://www.braintreepayments.com/gateway/customer-api
    """

    @staticmethod
    def all():
        """ Return a collection of all customers. """
        return Configuration.gateway().customer.all()

    @staticmethod
    def confirm_transparent_redirect(query_string):
        """
        Confirms a transparent redirect request.  It expects the query string from the
        redirect request.  The query string should _not_ include the leading "?" character. ::

            result = braintree.Customer.confirm_transparent_redirect_request("foo=bar&id=12345")
        """

        warnings.warn("Please use TransparentRedirect.confirm instead", DeprecationWarning)
        return Configuration.gateway().customer.confirm_transparent_redirect(query_string)

    @staticmethod
    def create(params={}):
        """
        Create a Customer::

            result = braintree.Customer.create({
                "company": "Some company",
                "first_name": "John"
            })
        """

        return Configuration.gateway().customer.create(params)

    @staticmethod
    def delete(customer_id):
        """
        Delete a customer, given a customer_id::

            result = braintree.Customer.delete("my_customer_id")
        """

        return Configuration.gateway().customer.delete(customer_id)

    @staticmethod
    def find(customer_id):
        """
        Find an customer, given a customer_id.  This does not return a result
        object.  This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>` if the provided customer_id
        is not found. ::

            customer = braintree.Customer.find("my_customer_id")
        """

        return Configuration.gateway().customer.find(customer_id)

    @staticmethod
    def search(*query):
        return Configuration.gateway().customer.search(*query)

    @staticmethod
    def tr_data_for_create(tr_data, redirect_url):
        """ Builds tr_data for creating a Customer. """

        return Configuration.gateway().customer.tr_data_for_create(tr_data, redirect_url)

    @staticmethod
    def tr_data_for_update(tr_data, redirect_url):
        """ Builds tr_data for updating a Customer. """

        return Configuration.gateway().customer.tr_data_for_update(tr_data, redirect_url)

    @staticmethod
    def transparent_redirect_create_url():
        """ Returns the url to use for creating Customers through transparent redirect. """

        warnings.warn("Please use TransparentRedirect.url instead", DeprecationWarning)
        return Configuration.gateway().customer.transparent_redirect_create_url()

    @staticmethod
    def transparent_redirect_update_url():
        """ Returns the url to use for updating Customers through transparent redirect. """

        warnings.warn("Please use TransparentRedirect.url instead", DeprecationWarning)
        return Configuration.gateway().customer.transparent_redirect_update_url()

    @staticmethod
    def update(customer_id, params={}):
        """
        Update an existing Customer by customer_id.  The params are similar to create::

            result = braintree.Customer.update("my_customer_id", {
                "last_name": "Smith"
            })
        """

        return Configuration.gateway().customer.update(customer_id, params)

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
            {"credit_card": CreditCard.signature("update_via_customer")},
            {"custom_fields": ["__any_key__"]}
        ]

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        if "credit_cards" in attributes:
            self.credit_cards = [CreditCard(gateway, credit_card) for credit_card in self.credit_cards]
        if "addresses" in attributes:
            self.addresses = [Address(gateway, address) for address in self.addresses]
