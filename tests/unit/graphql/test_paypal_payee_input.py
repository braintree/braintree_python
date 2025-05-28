from tests.test_helper import unittest
from braintree.graphql import PayPalPayeeInput

class TestPayPalPayeeInput(unittest.TestCase):
    def test_to_graphql_variables(self):
        input = (
            PayPalPayeeInput.builder()
            .client_id("1")
            .email_address("test@paypal.com")
            .build()
        )
        graphql_variables = input.to_graphql_variables()

        self.assertEqual("1", graphql_variables["clientId"])
        self.assertEqual("test@paypal.com", graphql_variables["emailAddress"])