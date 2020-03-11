from tests.test_helper import *

class TestGraphQLClient(unittest.TestCase):
    @raises(ServiceUnavailableError)
    def test_raise_exception_from_status_service_unavailable(self):
        response = {
            "errors": [
                {
                    "message": "error message",
                    "extensions": {
                        "errorClass": "SERVICE_AVAILABILITY"
                    }
                }
            ]
        }
        GraphQLClient.raise_exception_for_graphql_error(response)

    @raises(UpgradeRequiredError)
    def test_raise_exception_from_status_for_upgrade_required(self):
        response = {
            "errors": [
                {
                    "message": "error message",
                    "extensions": {
                        "errorClass": "UNSUPPORTED_CLIENT"
                    }
                }
            ]
        }
        GraphQLClient.raise_exception_for_graphql_error(response)

    @raises(TooManyRequestsError)
    def test_raise_exception_from_too_many_requests(self):
        response = {
            "errors": [
                {
                    "message": "error message",
                    "extensions": {
                        "errorClass": "RESOURCE_LIMIT"
                    }
                }
            ]
        }
        GraphQLClient.raise_exception_for_graphql_error(response)

    def test_does_not_raise_exception_from_validation_error(self):
        response = {
            "errors": [
                {
                    "message": "error message",
                    "extensions": {
                        "errorClass": "VALIDATION"
                    }
                }
            ]
        }
        GraphQLClient.raise_exception_for_graphql_error(response)

    @raises(ServerError)
    def test_raise_exception_from_validation_error_and_legitimate_error(self):
        response = {
            "errors": [
                {
                    "message": "error message",
                    "extensions": {
                        "errorClass": "VALIDATION"
                    }
                },
                {
                    "message": "error message 2",
                    "extensions": {
                        "errorClass": "INTERNAL"
                    }
                }
            ]
        }
        GraphQLClient.raise_exception_for_graphql_error(response)
