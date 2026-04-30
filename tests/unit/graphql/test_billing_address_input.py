from tests.test_helper import unittest
from braintree.graphql.inputs.billing_address_input import BillingAddressInput


class TestBillingAddressInput(unittest.TestCase):
    def test_billing_address_input_with_all_attributes(self):
        input = BillingAddressInput(
            street_address="123 Main St",
            extended_address="Apt 4B",
            locality="Mexico City",
            region="CDMX",
            postal_code="01000",
            country_code_alpha2="MX"
        )

        self.assertEqual("123 Main St", input._street_address)
        self.assertEqual("Apt 4B", input._extended_address)
        self.assertEqual("Mexico City", input._locality)
        self.assertEqual("CDMX", input._region)
        self.assertEqual("01000", input._postal_code)
        self.assertEqual("MX", input._country_code_alpha2)

    def test_to_graphql_variables_with_camel_case_keys(self):
        input = BillingAddressInput(
            street_address="123 Main St",
            locality="Mexico City",
            postal_code="01000",
            country_code_alpha2="MX"
        )

        expected_variables = {
            "streetAddress": "123 Main St",
            "locality": "Mexico City",
            "postalCode": "01000",
            "countryCode": "MX"
        }

        self.assertEqual(expected_variables, input.to_graphql_variables())

    def test_to_graphql_variables_omits_nil_values(self):
        input = BillingAddressInput(street_address="123 Main St")
        expected_variables = {"streetAddress": "123 Main St"}

        self.assertEqual(expected_variables, input.to_graphql_variables())
