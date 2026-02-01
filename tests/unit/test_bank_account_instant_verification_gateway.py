import unittest
from unittest.mock import Mock
from braintree.bank_account_instant_verification_gateway import BankAccountInstantVerificationGateway
from braintree.bank_account_instant_verification_jwt_request import BankAccountInstantVerificationJwtRequest


class TestBankAccountInstantVerificationGateway(unittest.TestCase):

    def setUp(self):
        self.mock_gateway = Mock()
        self.mock_config = Mock()
        self.mock_graphql_client = Mock()
        
        self.mock_gateway.config = self.mock_config
        self.mock_gateway.graphql_client = self.mock_graphql_client
        
        self.gateway = BankAccountInstantVerificationGateway(self.mock_gateway)

    def test_create_jwt_success(self):
        request = BankAccountInstantVerificationJwtRequest()
        request.business_name = "Test Business"
        request.return_url = "https://example.com/success"
        request.cancel_url = "https://example.com/cancel"

        mock_response = self._create_successful_jwt_response()
        self.mock_graphql_client.query.return_value = mock_response

        result = self.gateway.create_jwt(request)

        self.assertTrue(result.is_success)
        self.assertIsNotNone(result.bank_account_instant_verification_jwt)
        self.assertEqual("test-jwt-token", result.bank_account_instant_verification_jwt.jwt)

    def test_create_jwt_with_validation_errors(self):
        request = BankAccountInstantVerificationJwtRequest()
        request.business_name = ""
        request.return_url = "invalid-url"

        mock_response = self._create_error_response()
        self.mock_graphql_client.query.return_value = mock_response

        result = self.gateway.create_jwt(request)

        self.assertFalse(result.is_success)
        self.assertIsNotNone(result.errors)

    def test_create_jwt_graphql_query_uses_correct_mutation(self):
        request = BankAccountInstantVerificationJwtRequest()
        request.business_name = "Test Business"
        request.return_url = "https://example.com/success"

        mock_response = self._create_successful_jwt_response()
        self.mock_graphql_client.query.return_value = mock_response

        self.gateway.create_jwt(request)

        args, kwargs = self.mock_graphql_client.query.call_args
        query = args[0]
        self.assertIn("mutation CreateBankAccountInstantVerificationJwt", query)
        self.assertIn("createBankAccountInstantVerificationJwt(input: $input)", query)

    def test_create_jwt_minimal_request(self):
        request = BankAccountInstantVerificationJwtRequest()
        request.business_name = "Test Business"
        request.return_url = "https://example.com/success"

        mock_response = self._create_successful_jwt_response()
        self.mock_graphql_client.query.return_value = mock_response

        result = self.gateway.create_jwt(request)

        self.assertTrue(result.is_success)
        self.assertEqual("test-jwt-token", result.bank_account_instant_verification_jwt.jwt)

    def _create_successful_jwt_response(self):
        return {
            "data": {
                "createBankAccountInstantVerificationJwt": {
                    "jwt": "test-jwt-token"
                }
            }
        }

    def _create_error_response(self):
        return {
            "errors": [
                {
                    "message": "Validation error",
                    "extensions": {}
                }
            ]
        }


class TestBankAccountInstantVerificationJwtRequest(unittest.TestCase):

    def test_to_graphql_variables_includes_all_fields(self):
        request = BankAccountInstantVerificationJwtRequest()
        request.business_name("Test Business")
        request.return_url("https://example.com/success")
        request.cancel_url("https://example.com/cancel")

        variables = request.to_graphql_variables()

        self.assertIsNotNone(variables)
        self.assertEqual("Test Business", variables["businessName"])
        self.assertEqual("https://example.com/success", variables["returnUrl"])
        self.assertEqual("https://example.com/cancel", variables["cancelUrl"])

    def test_to_graphql_variables_only_includes_non_null_fields(self):
        request = BankAccountInstantVerificationJwtRequest()
        request.business_name("Test Business")
        request.return_url("https://example.com/success")

        variables = request.to_graphql_variables()
        
        self.assertEqual("Test Business", variables["businessName"])
        self.assertEqual("https://example.com/success", variables["returnUrl"])
        self.assertNotIn("cancelUrl", variables)

    def test_fluent_interface_returns_correct_instance(self):
        request = BankAccountInstantVerificationJwtRequest()
        
        result = (request
                 .business_name("Test Business")
                 .return_url("https://example.com/success")
                 .cancel_url("https://example.com/cancel"))

        self.assertIs(request, result)
        self.assertEqual("Test Business", request.get_business_name())
        self.assertEqual("https://example.com/success", request.get_return_url())
        self.assertEqual("https://example.com/cancel", request.get_cancel_url())