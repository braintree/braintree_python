import unittest
import tests.test_helper
import re
import random
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

    def test_create_can_specify_the_desired_token(self):
        token = str(random.randint(1, 1000000))
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "token": token
        })

        self.assertTrue(result.is_success)
        credit_card = result.credit_card
        self.assertEquals(token, credit_card.token)

    def test_create_with_billing_address(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "billing_address": {
                "street_address": "123 Abc Way",
                "locality": "Chicago",
                "region": "Illinois",
                "postal_code": "60622"
            }
        })

        self.assertTrue(result.is_success)
        address = result.credit_card.billing_address
        self.assertEquals("123 Abc Way", address.street_address)
        self.assertEquals("Chicago", address.locality)
        self.assertEquals("Illinois", address.region)
        self.assertEquals("60622", address.postal_code)

    def test_create_with_card_verification(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "5105105105105100",
            "expiration_date": "05/2009",
            "options": {"verify_card": True}
        })

        self.assertFalse(result.is_success)
        verification = result.credit_card_verification
        self.assertEquals("processor_declined", verification.status)
        self.assertEquals("2000", verification.processor_response_code)
        self.assertEquals("Do Not Honor", verification.processor_response_text)
        self.assertEquals("I", verification.cvv_response_code)
        self.assertEquals(None, verification.avs_error_response_code)
        self.assertEquals("I", verification.avs_postal_code_response_code)
        self.assertEquals("I", verification.avs_street_address_response_code)

    # it "verifes the credit card if options[verify_card]=true" do
    #   customer = Braintree::Customer.create!
    #   result = Braintree::CreditCard.create(
    #     :customer_id => customer.id,
    #     :number => Braintree::Test::CreditCardNumbers::FailsSandboxVerification::Visa,
    #     :expiration_date => "05/2009",
    #     :options => {:verify_card => true}
    #   )
    #   result.success?.should == false
    #   result.credit_card_verification.status.should == "processor_declined"
    #   result.credit_card_verification.processor_response_code.should == "2000"
    #   result.credit_card_verification.processor_response_text.should == "Do Not Honor"
    #   result.credit_card_verification.cvv_response_code.should == "I"
    #   result.credit_card_verification.avs_error_response_code.should == nil
    #   result.credit_card_verification.avs_postal_code_response_code.should == "I"
    #   result.credit_card_verification.avs_street_address_response_code.should == "I"
    # end

