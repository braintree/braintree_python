from tests.test_helper import *

from braintree.braintree_gateway import BraintreeGateway
from braintree.configuration import Configuration
from braintree.environment import Environment

class TestBraintreeGateway(unittest.TestCase):

    @staticmethod
    def get_gateway():
        config = Configuration("development", "integration_merchant_id",
                               public_key="integration_public_key",
                               private_key="integration_private_key")
        return BraintreeGateway(config)

    @unittest.skip("until we have a more stable ci env")
    def test_can_make_tokenize_credit_card_via_graphql(self):
        definition = """
          mutation ExampleServerSideSingleUseToken($input: TokenizeCreditCardInput!) {
            tokenizeCreditCard(input: $input) {
              paymentMethod {
                id
                usage
                details {
                  ... on CreditCardDetails {
                    bin
                    brandCode
                    last4
                    expirationYear
                    expirationMonth
                  }
                }
              }
            }
          }
        """
        variables = {
            "input" : {
                "creditCard" : {
                    "number" : "4005519200000004",
                    "expirationYear": "2024",
                    "expirationMonth": "05",
                    "cardholderName": "Joe Bloggs"
                }
            }
        }
        gateway = self.get_gateway()
        response = gateway.graphql_client.query(definition, variables)

        payment_method = response["data"]["tokenizeCreditCard"]["paymentMethod"]
        details = payment_method["details"]

        self.assertTrue("data" in response)
        self.assertTrue("id" in payment_method)
        self.assertEqual(details["bin"], "400551")
        self.assertEqual(details["last4"], "0004");
        self.assertEqual(details["brandCode"], "VISA");
        self.assertEqual(details["expirationMonth"], "05");
        self.assertEqual(details["expirationYear"], "2024");

    def test_can_make_graphql_queries_without_variables(self):
        definition = """
          query {
            ping
          }
        """
        gateway = self.get_gateway()
        response = gateway.graphql_client.query(definition)

        self.assertTrue("data" in response)
        self.assertTrue("ping" in response["data"])
        self.assertEqual("pong", response["data"]["ping"])
