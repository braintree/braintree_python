from unittest import TestCase

from braintree.configuration import Configuration
from braintree.environment import Environment

class TestGraphQLClient(TestCase):

    @staticmethod
    def get_graphql_client(environment):
        config = Configuration(environment, "integration_merchant_id",
                               public_key="integration_public_key",
                               private_key="integration_private_key")
        return config.graphql_client()

    def test_graphql_makes_valid_queries_without_variables(self):
        definition = '''
          query {
            ping
          }
        '''
        graphql_client = self.get_graphql_client(Environment.Development)
        response = graphql_client.query(definition)

        self.assertTrue("data" in response)
        self.assertTrue("ping" in response["data"])
        self.assertTrue("pong" == response["data"]["ping"])

    def test_graphql_makes_valid_queries_with_variables(self):
        definition = '''
          mutation CreateClientToken($input: CreateClientTokenInput!) {
            createClientToken(input: $input) {
            clientToken
            }
          }
        '''

        variables = {
            "input": {
                "clientToken": {
                    "merchantAccountId": "ABC123"
                }
            }
        }

        graphql_client = self.get_graphql_client(Environment.Development)
        response = graphql_client.query(definition, variables)

        self.assertTrue("data" in response)
        self.assertTrue("createClientToken" in response["data"])
        self.assertTrue("clientToken" in response["data"]["createClientToken"])
