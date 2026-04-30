from tests.test_helper import unittest
from braintree.graphql.inputs.payer_info_input import PayerInfoInput
from braintree.graphql.inputs.billing_address_input import BillingAddressInput


class TestPayerInfoInput(unittest.TestCase):
    def test_payer_info_input_with_all_attributes(self):
        input = PayerInfoInput(
            given_name="John",
            surname="Doe",
            phone_number="912345678",
            phone_country_code="351",
            billing_address={
                "street_address": "123 Main St",
                "locality": "Lisbon"
            }
        )

        self.assertEqual("John", input._given_name)
        self.assertEqual("Doe", input._surname)
        self.assertEqual("912345678", input._phone_number)
        self.assertEqual("351", input._phone_country_code)
        self.assertIsInstance(input._billing_address, BillingAddressInput)

    def test_to_graphql_variables_with_billing_address(self):
        input = PayerInfoInput(
            given_name="John",
            surname="Doe",
            email="john@example.com",
            phone_country_code="1",
            billing_address={
                "street_address": "123 Main St",
                "locality": "Lisbon"
            }
        )

        variables = input.to_graphql_variables()

        self.assertEqual("John", variables["givenName"])
        self.assertEqual("Doe", variables["surname"])
        self.assertEqual("john@example.com", variables["email"])
        self.assertEqual("1", variables["phoneCountryCode"])
        self.assertIn("billingAddress", variables)
        self.assertEqual("123 Main St", variables["billingAddress"]["streetAddress"])

    def test_handles_nil_billing_address(self):
        input = PayerInfoInput(given_name="John", surname="Doe")
        variables = input.to_graphql_variables()

        self.assertEqual("John", variables["givenName"])
        self.assertEqual("Doe", variables["surname"])
        self.assertNotIn("billingAddress", variables)
