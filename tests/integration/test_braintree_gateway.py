from unittest import TestCase

from braintree.braintree_gateway import BraintreeGateway
from braintree.configuration import Configuration
from braintree.environment import Environment

class TestBraintreeGateway(TestCase):

    @staticmethod
    def get_gateway():
        config = Configuration("development", "integration_merchant_id",
                               public_key="integration_public_key",
                               private_key="integration_private_key")
        return BraintreeGateway(config)

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
