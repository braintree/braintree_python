from braintree.bank_account_instant_verification_jwt import BankAccountInstantVerificationJwt
from braintree.successful_result import SuccessfulResult
from braintree.error_result import ErrorResult
from braintree.exceptions.unexpected_error import UnexpectedError
from braintree.util.graphql_client import GraphQLClient


class BankAccountInstantVerificationGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = self.gateway.config
        self.graphql_client = self.gateway.graphql_client

    CREATE_JWT_MUTATION = """
        mutation CreateBankAccountInstantVerificationJwt($input: CreateBankAccountInstantVerificationJwtInput!) {
            createBankAccountInstantVerificationJwt(input: $input) {
                jwt
            }
        }
    """

    def create_jwt(self, request):
        try: 
            variables = dict({"input": request.to_graphql_variables()})
            response = self.graphql_client.query(self.CREATE_JWT_MUTATION, variables)
            
            if "errors" in response:
                errors = GraphQLClient.get_validation_errors(response)
                return ErrorResult(self.gateway, {"errors": errors, "message": "Validation errors were found"})

            data = response.get("data", {})
            result = data.get("createBankAccountInstantVerificationJwt", {})
            
            jwt = result.get("jwt")

            if jwt is None:
                raise UnexpectedError("Couldn't parse response: missing jwt")

            jwt_object = BankAccountInstantVerificationJwt(jwt)
            return SuccessfulResult({"bank_account_instant_verification_jwt": jwt_object})

        except (KeyError, TypeError) as e:
            raise UnexpectedError("Couldn't parse response: " + str(e))