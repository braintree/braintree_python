from typing import Dict
import braintree
from braintree.error_result import ErrorResult
from braintree.exceptions.unexpected_error import UnexpectedError
from braintree.successful_result import SuccessfulResult
from braintree.util.graphql_client import GraphQLClient
from braintree.graphql import (
    CreateCustomerSessionInput,
    UpdateCustomerSessionInput,
    CustomerRecommendations,
    CustomerRecommendationsInput,
    CustomerRecommendationsPayload,
    PaymentOptions,
)


class CustomerSessionGateway:
    """
    Creates and manages PayPal customer sessions.
    """
    def __init__(self, gateway):
        self.gateway = gateway
        self.graphql_client = self.gateway.graphql_client

    def create_customer_session(self, customer_session_input: CreateCustomerSessionInput):
        """
        Creates a new customer session.

        Example:
          customer_session = (
            CustomerSessionInput
            .builder()
            .email("test@example.com")
            .build()
          )

          create_input = (
            CreateCustomerSessionInput
            .builder()
            .customer(customer_session)
            .build()
          )

          result = gateway.customer_session.create_customer_session(create_input)
    
          if result.is_success:
            print(result.session_id)

        Args:
            CreateCustomerSessionInput: Input object for creating a customer session.
        
        Returns:
            (Successful|Error)Result: A result object with session ID if successful, or errors otherwise.

        Raises:
            UnexpectedError: If there is an unexpected error during the process.
        """
        mutation = """
            mutation CreateCustomerSession($input: CreateCustomerSessionInput!) {
              createCustomerSession(input: $input) {
                sessionId
              }
            }
        """
        variables = dict({"input": customer_session_input.to_graphql_variables()})
        return  self._execute_mutation(mutation, variables, "createCustomerSession")


    def update_customer_session(self, update_customer_session_input: UpdateCustomerSessionInput):
        """
        Updates an existing customer session.

        Example:
          customer_session = (
            CustomerSessionInput
            .builder()
            .email("test@example.com")
            .build()
          )

          update_input = (
            UpdateCustomerSessionInput
            .builder(session_id)
            .customer(customer_session)
            .build()
          )

          result = gateway.customer_session.update_customer_session(update_input)
    
          if result.is_success:
            print(result.session_id)

        Args:
            UpdateCustomerSessionInput: Input object for updating a customer session.
        
        Returns:
            (Successful|Error)Result: A result object with session ID if successful, or errors otherwise.

        Raises:
            UnexpectedError: If there is an unexpected error during the process.
        """
        mutation = """
            mutation UpdateCustomerSession($input: UpdateCustomerSessionInput!) {
              updateCustomerSession(input: $input) {
                sessionId
              }
            }
        """
        variables = dict({"input": update_customer_session_input.to_graphql_variables()})
        return self._execute_mutation(mutation, variables, "updateCustomerSession")

    def get_customer_recommendations(self, customer_recommendations_input: CustomerRecommendationsInput):
        """
        Retrieves customer recommendations associated with a customer session.

        Example:

          recommendations_input = (
            CustomerRecommendationsInput
              .builder(session_id, [Recommendations.PAYMENT_RECOMMENDATIONS])
              .build()
          )

          result = gateway.customer_session.get_customer_recommendations(recommendations_input)
         
          if result.is_success:
            print(result.customer_recommendations)

        Args:
            CustomerRecommendationsInput: Input object for retrieving customer recommendations.
        
        Returns:
            (Successful|Error)Result: A result object containing a CustomerRecommendationsPayload and a success flag if successful, or errors otherwise.

        Raises:
            UnexpectedError: If there is an unexpected error during the process.
        """
        query = """
            query CustomerRecommendations($input: CustomerRecommendationsInput!) {
                customerRecommendations(input: $input) {
                  isInPayPalNetwork
                  recommendations {
                    ... on PaymentRecommendations {
                      paymentOptions {
                        paymentOption
                        recommendedPriority
                      }
                    }
                  }
                }
              }
        """
        variables = dict({"input": customer_recommendations_input.to_graphql_variables()})

        response = self.graphql_client.query(query, variables)
        errors = GraphQLClient.get_validation_errors(response)
        if errors:
            return ErrorResult(self.gateway, {"errors": errors, "message": "Validation errors were found."})
        try:
            recommendations_payload = self._extract_customer_recommendations_payload(response)
            return SuccessfulResult({"customer_recommendations": recommendations_payload})
        except KeyError:
            raise UnexpectedError("Couldn't parse response")

    def _execute_mutation(self, mutation: str, variables: Dict, operation: str):
        response = self.graphql_client.query(mutation, variables)
        errors = GraphQLClient.get_validation_errors(response)
        if errors:
            return ErrorResult(self.gateway, {"errors": errors, "message": "Validation errors were found."})
        try:
            session_id = response["data"][operation]["sessionId"]
            return  SuccessfulResult({"session_id": session_id})
        except KeyError:
            raise UnexpectedError("Couldn't parse response")

    def _extract_customer_recommendations_payload(self, response):
        customer_recommendations = response["data"]["customerRecommendations"]

        is_in_paypal_network = customer_recommendations["isInPayPalNetwork"]
        recommendations = [] if customer_recommendations["recommendations"] is None else customer_recommendations["recommendations"]["paymentOptions"]
        payment_options = [
            PaymentOptions(
                    recommendation_data["paymentOption"],
                    recommendation_data["recommendedPriority"]
            ) 
            for recommendation_data in recommendations
        ]

        recommendations_union = CustomerRecommendations(payment_options)
        return CustomerRecommendationsPayload(is_in_paypal_network, recommendations_union)



