import unittest
import tests.test_helper
import re
from braintree.customer import Customer
from braintree.address import Address

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

