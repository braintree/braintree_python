import unittest
import tests.test_helper
from nose.tools import raises
import re
from braintree.customer import Customer
from braintree.address import Address
from braintree.exceptions.not_found_error import NotFoundError

class TestAddress(unittest.TestCase):
    def test_create_returns_successful_result_if_valid(self):
        customer = Customer.create().customer
        result = Address.create({
            "customer_id": customer.id,
            "first_name": "Ben",
            "last_name": "Moore",
            "company": "Moore Co.",
            "street_address": "1811 E Main St",
            "extended_address": "Suite 200",
            "locality": "Chicago",
            "region": "Illinois",
            "postal_code": "60622",
            "country_name": "United States of America"
        })

        self.assertTrue(result.is_success)
        address = result.address
        self.assertEquals(customer.id, address.customer_id)
        self.assertEquals("Ben", address.first_name)
        self.assertEquals("Moore", address.last_name)
        self.assertEquals("Moore Co.", address.company)
        self.assertEquals("1811 E Main St", address.street_address)
        self.assertEquals("Suite 200", address.extended_address)
        self.assertEquals("Chicago", address.locality)
        self.assertEquals("Illinois", address.region)
        self.assertEquals("60622", address.postal_code)
        self.assertEquals("United States of America", address.country_name)

    def test_error_response_if_invalid(self):
        customer = Customer.create().customer
        result = Address.create({
            "customer_id": customer.id,
            "country_name": "United States of Invalid"
        })

        self.assertFalse(result.is_success)
        self.assertEquals("91803", result.errors.for_object("address").on("country_name")[0].code)

    def test_delete_with_valid_customer_id_and_address_id(self):
        customer = Customer.create().customer
        address = Address.create({"customer_id": customer.id, "street_address": "123 Main St."}).address
        result = Address.delete(customer.id, address.id)

        self.assertTrue(result.is_success)

    @raises(NotFoundError)
    def test_delete_with_valid_customer_id_and_non_existing_address(self):
        customer = Customer.create().customer
        result = Address.delete(customer.id, "notreal")

    def test_find_with_valid_customer_id_and_address_id(self):
        customer = Customer.create().customer
        address = Address.create({"customer_id": customer.id, "street_address": "123 Main St."}).address
        found_address = Address.find(customer.id, address.id)

        self.assertEquals(address.street_address, found_address.street_address)

    @raises(NotFoundError)
    def test_find_with_invalid_customer_id_and_address_id(self):
        customer = Customer.create().customer
        address = Address.create({"customer_id": customer.id, "street_address": "123 Main St."}).address
        Address.find("notreal", "badaddress")

