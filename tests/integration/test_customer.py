import unittest
import re
import tests.test_helper
from nose.tools import raises
from braintree.customer import Customer
from braintree.exceptions.not_found_error import NotFoundError

class TestCustomer(unittest.TestCase):
    def test_create(self):
        result = Customer.create({
            "first_name": "Bill",
            "last_name": "Gates",
            "company": "Microsoft",
            "email": "bill@microsoft.com",
            "phone": "312.555.1234",
            "fax": "614.555.5678",
            "website": "www.microsoft.com"
        })

        self.assertTrue(result.is_success)
        customer = result.customer

        self.assertEqual("Bill", customer.first_name)
        self.assertEqual("Gates", customer.last_name)
        self.assertEqual("Microsoft", customer.company)
        self.assertEqual("bill@microsoft.com", customer.email)
        self.assertEqual("312.555.1234", customer.phone)
        self.assertEqual("614.555.5678", customer.fax)
        self.assertEqual("www.microsoft.com", customer.website)
        self.assertNotEqual(None, customer.id)
        self.assertNotEqual(None, re.search("\A\d{6,7}\Z", customer.id))

    def test_create_with_no_attributes(self):
        result = Customer.create()
        self.assertTrue(result.is_success)
        self.assertNotEqual(None, result.customer.id)

    def test_create_returns_an_error_response_if_invalid(self):
        result = Customer.create({
            "email": "@invalid.com",
        })

        self.assertFalse(result.is_success)
        self.assertEquals(1, result.errors.size)
        self.assertEquals("81604", result.errors.for_object("customer").on("email")[0].code)

    def test_create_customer_and_payment_method_at_the_same_time(self):
        result = Customer.create({
            "first_name": "Mike",
            "last_name": "Jones",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "cvv": "100"
            }
        })

        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertEqual("Mike", customer.first_name)
        self.assertEqual("Jones", customer.last_name)

        credit_card = customer.credit_cards[0]
        self.assertEqual("411111", credit_card.bin)
        self.assertEqual("1111", credit_card.last_4)
        self.assertEqual("05/2010", credit_card.expiration_date)

    def test_create_customer_and_verify_payment_method(self):
        result = Customer.create({
            "first_name": "Mike",
            "last_name": "Jones",
            "credit_card": {
                "number": "4222222222222",
                "expiration_date": "05/2010",
                "cvv": "100",
                "options": {"verify_card": True}
            }
        })

        self.assertFalse(result.is_success)
        self.assertEquals("processor_declined", result.credit_card_verification.status)

    def test_create_customer_with_payment_method_and_billing_address(self):
        result = Customer.create({
            "first_name": "Mike",
            "last_name": "Jones",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "cvv": "100",
                "billing_address": {
                    "street_address": "123 Abc Way",
                    "locality": "Chicago",
                    "region": "Illinois",
                    "postal_code": "60622"
                }
            }
        })

        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertEqual("Mike", customer.first_name)
        self.assertEqual("Jones", customer.last_name)

        address = customer.credit_cards[0].billing_address
        self.assertEqual("123 Abc Way", address.street_address)
        self.assertEqual("Chicago", address.locality)
        self.assertEqual("Illinois", address.region)
        self.assertEqual("60622", address.postal_code)

    def test_create_with_customer_fields(self):
        result = Customer.create({
            "first_name": "Mike",
            "last_name": "Jones",
            "custom_fields": {
                "store_me": "custom value"
            }
        })

        self.assertTrue(result.is_success)
        self.assertEquals("custom value", result.customer.custom_fields["store_me"])

    def test_create_returns_nested_errors(self):
        result = Customer.create({
            "email": "invalid",
            "credit_card": {
                "number": "invalid",
                "billing_address": {
                    "country_name": "invalid"
                }
            }
        })

        self.assertFalse(result.is_success)
        self.assertEquals("81604", result.errors.for_object("customer").on("email")[0].code)
        self.assertEquals("81716", result.errors.for_object("customer").for_object("credit_card").on("number")[0].code)
        self.assertEquals("91803", result.errors.for_object("customer").for_object("credit_card").for_object("billing_address").on("country_name")[0].code)

    def test_create_returns_errors_if_custom_fields_are_not_registered(self):
        result = Customer.create({
            "first_name": "Jack",
            "last_name": "Kennedy",
            "custom_fields": {
                "spouse_name": "Jacqueline"
            }
        })

        self.assertFalse(result.is_success)
        self.assertEquals("91602", result.errors.for_object("customer").on("custom_fields")[0].code)

    def test_delete_with_valid_customer(self):
        customer = Customer.create().customer
        result = Customer.delete(customer.id)

        self.assertTrue(result.is_success)

    @raises(NotFoundError)
    def test_delete_with_invalid_customer(self):
        customer = Customer.create().customer
        Customer.delete(customer.id)
        Customer.delete(customer.id)

    def test_find_with_valid_customer(self):
        customer = Customer.create({
            "first_name": "Joe",
            "last_name": "Cool"
        }).customer

        found_customer = Customer.find(customer.id)
        self.assertEquals(customer.id, found_customer.id)
        self.assertEquals(customer.first_name, found_customer.first_name)
        self.assertEquals(customer.last_name, found_customer.last_name)

    def test_find_with_invalid_customer(self):
        try:
            Customer.find("badid")
            self.assertTrue(False)
        except NotFoundError as e:
            self.assertEquals("customer with id badid not found", str(e))

