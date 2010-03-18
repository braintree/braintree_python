import unittest
import tests.test_helper
from nose.tools import raises
import re
import random
from datetime import datetime
from braintree.error_codes import ErrorCodes
from braintree.customer import Customer
from braintree.credit_card import CreditCard
from braintree.exceptions.not_found_error import NotFoundError

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
        self.assertTrue(re.search("\A\w{4,5}\Z", credit_card.token) != None)
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
            "number": "4222222222222",
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

    def test_create_with_card_verification_set_to_false(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4222222222222",
            "expiration_date": "05/2009",
            "options": {"verify_card": False}
        })

        self.assertTrue(result.is_success)

    def test_create_with_invalid_invalid_options(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "invalid_date",
        })

        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.CreditCard.ExpirationDateIsInvalid, result.errors.for_object("credit_card").on("expiration_date")[0].code)

    def test_update_with_valid_options(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe"
        }).credit_card

        result = CreditCard.update(credit_card.token, {
            "number": "5105105105105100",
            "expiration_date": "06/2010",
            "cvv": "123",
            "cardholder_name": "Jane Jones"
        })

        self.assertTrue(result.is_success)
        credit_card = result.credit_card
        self.assertTrue(re.search("\A\w{4,5}\Z", credit_card.token) != None)
        self.assertEquals("510510", credit_card.bin)
        self.assertEquals("5100", credit_card.last_4)
        self.assertEquals("06", credit_card.expiration_month)
        self.assertEquals("2010", credit_card.expiration_year)
        self.assertEquals("06/2010", credit_card.expiration_date)
        self.assertEquals("Jane Jones", credit_card.cardholder_name)

    def test_update_verifies_card_if_option_is_provided(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe"
        }).credit_card

        result = CreditCard.update(credit_card.token, {
            "number": "4222222222222",
            "expiration_date": "06/2010",
            "cvv": "123",
            "cardholder_name": "Jane Jones",
            "options": {"verify_card": True}
        })

        self.assertFalse(result.is_success)
        self.assertEquals("processor_declined", result.credit_card_verification.status)

    def test_update_billing_address(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "billing_address": {
                "street_address": "321 Xyz Way",
                "locality": "Chicago",
                "region": "Illinois",
                "postal_code": "60621"
            }
        }).credit_card

        result = CreditCard.update(credit_card.token, {
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

    def test_update_returns_error_if_invalid(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009"
        }).credit_card

        result = CreditCard.update(credit_card.token, {
            "expiration_date": "invalid_date"
        })

        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.CreditCard.ExpirationDateIsInvalid, result.errors.for_object("credit_card").on("expiration_date")[0].code)

    def test_delete_with_valid_token(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009"
        }).credit_card

        result = CreditCard.delete(credit_card.token)
        self.assertTrue(result.is_success)

    @raises(NotFoundError)
    def test_delete_raises_error_when_deleting_twice(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009"
        }).credit_card

        CreditCard.delete(credit_card.token)
        CreditCard.delete(credit_card.token)

    @raises(NotFoundError)
    def test_delete_with_invalid_token(self):
        result = CreditCard.delete("notreal")

    def test_find_with_valid_token(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009"
        }).credit_card

        found_credit_card = CreditCard.find(credit_card.token)
        self.assertTrue(re.search("\A\w{4,5}\Z", credit_card.token) != None)
        self.assertEquals("411111", credit_card.bin)
        self.assertEquals("1111", credit_card.last_4)
        self.assertEquals("05", credit_card.expiration_month)
        self.assertEquals("2009", credit_card.expiration_year)
        self.assertEquals("05/2009", credit_card.expiration_date)

    def test_find_with_invalid_token(self):
        try:
            CreditCard.find("bad_token")
            self.assertTrue(False)
        except Exception as e:
            self.assertEquals("payment method with token bad_token not found", str(e))

