from braintree.error_result import ErrorResult
from braintree.exceptions.authentication_error import AuthenticationError
from braintree.exceptions.authorization_error import AuthorizationError
from braintree.exceptions.not_found_error import NotFoundError
from braintree.exceptions.unexpected_error import UnexpectedError
from braintree.successful_result import SuccessfulResult
from braintree.util.graphql_client import GraphQLClient
from braintree.local_payment_context import LocalPaymentContext

class LocalPaymentContextGateway:
    """
    Creates and manages local payment contexts.
    """

    CREATE_LOCAL_PAYMENT_CONTEXT = """
        mutation CreateLocalPaymentContext($input: CreateLocalPaymentContextInput!) {
            createLocalPaymentContext(input: $input) {
                paymentContext {
                    id
                    legacyId
                    type
                    paymentId
                    approvalUrl
                    merchantAccountId
                    orderId
                    createdAt
                    transactedAt
                    approvedAt
                    amount {
                        value
                        currencyCode
                    }
                }
            }
        }
    """

    FIND_LOCAL_PAYMENT_CONTEXT = """
        query Node($id: ID!) {
            node(id: $id) {
                ... on LocalPaymentContext {
                    id
                    legacyId
                    type
                    amount {
                        value
                        currencyIsoCode
                    }
                    approvalUrl
                    merchantAccountId
                    transactedAt
                    approvedAt
                    createdAt
                    updatedAt
                    expiredAt
                    paymentId
                    orderId
                }
            }
        }
    """

    def __init__(self, gateway):
        self.gateway = gateway
        self.graphql_client = self.gateway.graphql_client

    def create(self, input):
        """
        Creates a local payment context.

        Args:
            input: CreateLocalPaymentContextInput object

        Returns:
            SuccessfulResult or ErrorResult
        """
        variables = {"input": input.to_graphql_variables()}

        try:
            response = self.graphql_client.query(self.CREATE_LOCAL_PAYMENT_CONTEXT, variables)
            errors = GraphQLClient.get_validation_errors(response)

            if errors:
                return ErrorResult(self.gateway, {"errors": errors, "message": "Validation errors were found."})
            else:
                payment_context = self._extract_payment_context(response)
                return SuccessfulResult({"payment_context": payment_context})
        except (AuthenticationError, AuthorizationError):
            raise
        except Exception as e:
            raise UnexpectedError(str(e))

    def find(self, id):
        """
        Finds a local payment context by ID.

        Args:
            id: The payment context ID

        Returns:
            SuccessfulResult or ErrorResult

        Raises:
            NotFoundError: If the payment context is not found
        """
        variables = {"id": id}

        try:
            response = self.graphql_client.query(self.FIND_LOCAL_PAYMENT_CONTEXT, variables)
            errors = GraphQLClient.get_validation_errors(response)

            if errors:
                return ErrorResult(self.gateway, {"errors": errors, "message": "Validation errors were found."})
            else:
                payment_context = self._extract_node_payment_context(response)
                return SuccessfulResult({"payment_context": payment_context})
        except (NotFoundError, AuthenticationError, AuthorizationError):
            raise
        except Exception as e:
            raise UnexpectedError(str(e))

    def _extract_payment_context(self, response):
        """Extract payment context from create mutation response"""
        context_hash = self._get_value(response, "data.createLocalPaymentContext.paymentContext")
        return LocalPaymentContext({"response": {"paymentContext": context_hash}})

    def _extract_node_payment_context(self, response):
        """Extract payment context from node query response"""
        node_hash = self._get_value(response, "data.node")

        if node_hash is None:
            raise NotFoundError("Payment context not found")

        return LocalPaymentContext({"response": {"paymentContext": node_hash}})

    def _get_value(self, response, key):
        """Get a value from nested response dictionary"""
        map_obj = response
        key_parts = key.split(".")

        for sub_key in key_parts[:-1]:
            map_obj = self._pop_value(map_obj, sub_key)
            if not isinstance(map_obj, dict):
                raise UnexpectedError("Couldn't parse response")

        return self._pop_value(map_obj, key_parts[-1])

    def _pop_value(self, map_obj, key):
        """Pop a value from dictionary"""
        if key in map_obj:
            return map_obj[key]
        else:
            raise UnexpectedError("Couldn't parse response")
