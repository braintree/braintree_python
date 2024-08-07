from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.resource import Resource
from braintree.configuration import Configuration

class Address(Resource):
    """
    A class representing Braintree Address objects.

    An example of creating an address with all available fields::

        customer = braintree.Customer.create().customer
        result = braintree.Address.create({
            "company": "Braintree",
            "country_name": "United States of America",
            "customer_id": customer.id,
            "extended_address": "Apartment 1",
            "first_name": "John",
            "international_phone": { "country_code": "1", "national_number": "3121234567" },
            "last_name": "Doe",
            "locality": "Chicago",
            "phone_number": "312-123-4567",
            "postal_code": "60606",
            "region": "IL",
            "street_address": "111 First Street"
        })

        print(result.customer.first_name)
        print(result.customer.last_name)
    """

    def __repr__(self):
        detail_list = [
            "company",
            "country_code_alpha2",
            "country_code_alpha3",
            "country_code_numeric",
            "country_name",
            "customer_id",
            "extended_address",
            "first_name",
            "international_phone",
            "last_name",
            "locality",
            "phone_number",
            "postal_code",
            "region",
            "shipping_method",
            "street_address"
        ]
        return super(Address, self).__repr__(detail_list)

    # NEXT_MAJOR_VERSION this can be an enum! they were added as of python 3.4 and we support 3.5+
    class ShippingMethod(object):
        """
        Constants representing shipping methods for shipping addresses. Available types are:

        * braintree.Address.ShippingMethod.SameDay
        * braintree.Address.ShippingMethod.NextDay
        * braintree.Address.ShippingMethod.Priority
        * braintree.Address.ShippingMethod.Ground
        * braintree.Address.ShippingMethod.Electronic
        * braintree.Address.ShippingMethod.ShipToStore
        * braintree.Address.ShippingMethod.PickupInStore
        """
        SameDay     = "same_day"
        NextDay     = "next_day"
        Priority    = "priority"
        Ground      = "ground"
        Electronic  = "electronic"
        ShipToStore = "ship_to_store"
        PickupInStore = "pickup_in_store"

    @staticmethod
    def create(params=None):
        """
        Create an Address.

        A customer_id is required::

            customer = braintree.Customer.create().customer
            result = braintree.Address.create({
                "customer_id": customer.id,
                "first_name": "John",
                ...
            })

        """
        if params is None:
            params = {}
        return Configuration.gateway().address.create(params)

    @staticmethod
    def delete(customer_id, address_id):
        """
        Delete an address

        Given a customer_id and address_id::

            result = braintree.Address.delete("my_customer_id", "my_address_id")

        """

        return Configuration.gateway().address.delete(customer_id, address_id)

    @staticmethod
    def find(customer_id, address_id):
        """
        Find an address, given a customer_id and address_id. This does not return
        a result object. This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>` if the provided
        customer_id/address_id are not found. ::

            address = braintree.Address.find("my_customer_id", "my_address_id")
        """
        return Configuration.gateway().address.find(customer_id, address_id)

    @staticmethod
    def update(customer_id, address_id, params=None):
        """
        Update an existing Address.

        A customer_id and address_id are required::

            result = braintree.Address.update("my_customer_id", "my_address_id", {
                "first_name": "John"
            })

        """
        if params is None:
            params = {}
        return Configuration.gateway().address.update(customer_id, address_id, params)

    @staticmethod
    def create_signature():
        return ["company", "country_code_alpha2", "country_code_alpha3", "country_code_numeric",
                "country_name", "customer_id", "extended_address", "first_name",
                {"international_phone": ["country_code", "national_number"]},
                "last_name", "locality", "phone_number",
                "postal_code", "region", "street_address"]

    @staticmethod
    def update_signature():
        return Address.create_signature()
