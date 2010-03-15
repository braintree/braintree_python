import unittest
import tests.test_helper
from braintree.customer import Customer

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

    def test_create_with_no_attributes(self):
        result = Customer.create()
        self.assertTrue(result.is_success)

