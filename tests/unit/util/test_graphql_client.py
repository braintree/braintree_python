import unittest
from braintree.util.graphql_client import GraphQLClient


class TestGraphQLClient(unittest.TestCase):

    def test_get_validation_errors_returns_none_when_no_errors(self):
        response = {"data": {}}
        self.assertIsNone(GraphQLClient.get_validation_errors(response))

    def test_get_validation_errors_returns_none_when_errors_not_a_list(self):
        response = {"errors": "some string"}
        self.assertIsNone(GraphQLClient.get_validation_errors(response))

    def test_get_validation_errors_returns_formatted_errors(self):
        response = {
            "errors": [
                {"message": "Error 1", "extensions": {"legacyCode": "123"}},
                {"message": "Error 2", "extensions": {}},  
            ]
        }

        expected_errors = {
            "errors": [
                {"attribute": "", "code": "123", "message": "Error 1"},
                {"attribute": "", "code": None, "message": "Error 2"},
            ]
        }

        self.assertEqual(GraphQLClient.get_validation_errors(response), expected_errors)


