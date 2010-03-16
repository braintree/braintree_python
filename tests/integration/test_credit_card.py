import unittest
import tests.test_helper
import re
from datetime import datetime
from braintree.customer import Customer
from braintree.credit_card import CreditCard

class TestCreditCard(unittest.TestCase):
    def test_create_adds_credit_card_to_existing_customer(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertTrue(result.is_success)
        credit_card = result.credit_card
        self.assertTrue(re.match("\A\w{4,5}\Z", credit_card.token) != None)
        self.assertEquals("411111", credit_card.bin)
        self.assertEquals("1111", credit_card.last_4)
        self.assertEquals("05", credit_card.expiration_month)
        self.assertEquals("2009", credit_card.expiration_year)
        self.assertEquals("05/2009", credit_card.expiration_date)
        self.assertEquals("John Doe", credit_card.cardholder_name)

