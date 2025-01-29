from braintree.braintree_gateway import BraintreeGateway
from braintree.customer_session_gateway import CustomerSessionGateway
from braintree.graphql import (
    CreateCustomerSessionInput,
    CustomerSessionInput,
    UpdateCustomerSessionInput,
    CustomerRecommendationsInput,
    CustomerRecommendations,
    CustomerRecommendationsPayload,
    PaymentOptions,
)
from braintree.error_result import ErrorResult
from braintree.successful_result import SuccessfulResult
from unittest.mock import patch, MagicMock
import unittest
from tests.test_helper import *


class TestCustomerSessionGateway(unittest.TestCase):
    def setUp(self):
        self.gateway = BraintreeGateway(None)
        self.mock_graphql_client = MagicMock()
        self.gateway.graphql_client = self.mock_graphql_client
        self.customer_session_gateway = CustomerSessionGateway(self.gateway)

    def test_create_customer_session_returns_successful_result(self):
        self.mock_graphql_client.query.return_value = {
            "data": {"createCustomerSession": {"sessionId": "session-id"}}
        }
        input_data = (
            CreateCustomerSessionInput.builder()
            .merchant_account_id("merchant_account_id")
            .session_id("session_id")
            .build()
        )

        result = self.customer_session_gateway.create_customer_session(input_data)

        self.assertTrue(result.is_success)
        self.assertEqual("session-id", result.session_id)

    def test_create_customer_session_returns_error_result(self):
        errors = {
            "errors": [
                {"message": "Error 1", "extensions": {"legacyCode": "123"}},
                {"message": "Error 2", "extensions": {}},
            ]
        }

        self.mock_graphql_client.query.return_value = errors
        input_data = (
            CreateCustomerSessionInput.builder()
            .merchant_account_id("merchant_account_id")
            .session_id("session_id")
            .build()
        )

        result = self.customer_session_gateway.create_customer_session(input_data)
        self.assertFalse(result.is_success)
        self.assertEqual('123', result.errors.deep_errors[0].code)
        self.assertEqual(None, result.errors.deep_errors[1].code)
        self.assertEqual('Error 1', result.errors.deep_errors[0].message)
        self.assertEqual('Error 2', result.errors.deep_errors[1].message)


    def test_update_customer_session_returns_successful_result(self):
        self.mock_graphql_client.query.return_value = {"data": {"updateCustomerSession": {"sessionId": "session-id"}}}
        input_data = UpdateCustomerSessionInput.builder("session_id").build()

        result = self.customer_session_gateway.update_customer_session(input_data)

        self.assertTrue(result.is_success)
        self.assertEqual("session-id", result.session_id)

    def test_update_customer_session_returns_error_result(self):
        errors = {
            "errors": [
                {"message": "Error 1", "extensions": {"legacyCode": "123"}}
            ]
        }

        self.mock_graphql_client.query.return_value = errors
        input_data = UpdateCustomerSessionInput.builder("session_id").build()

        result = self.customer_session_gateway.update_customer_session(input_data)
        self.assertFalse(result.is_success)
        self.assertEqual('123', result.errors.deep_errors[0].code)
        self.assertEqual('Error 1', result.errors.deep_errors[0].message)


    def test_get_customer_recommendations_returns_successful_result(self):
        response = {
            "data": {
                "customerRecommendations": {
                    "isInPayPalNetwork": True,
                    "recommendations": {
                        "paymentOptions": [{"paymentOption": "PAYPAL", "recommendedPriority": 1}]
                    }
                }
            }
        }
        self.mock_graphql_client.query.return_value = response

        customer_recommendations_input = CustomerRecommendationsInput.Builder("session-id", []).merchant_account_id("merchant-account-id").build()
        result = self.customer_session_gateway.get_customer_recommendations(customer_recommendations_input)

        self.assertTrue(result.is_success)
        self.assertTrue(result.customer_recommendations.is_in_paypal_network)
        payment_options = result.customer_recommendations.recommendations.payment_options
        self.assertEqual(len(payment_options), 1)
        self.assertEqual(payment_options[0].payment_option, "PAYPAL")
        self.assertEqual(payment_options[0].recommended_priority, 1)

    def test_get_customer_recommendations_returns_error_result(self):
        errors = {
            "errors": [
                {"message": "Error 1", "extensions": {"legacyCode": "123"}}
            ]
        }

        self.mock_graphql_client.query.return_value = errors
        customer_recommendations_input = CustomerRecommendationsInput.Builder("session-id", []).merchant_account_id("merchant-account-id").build()

        result = self.customer_session_gateway.get_customer_recommendations(customer_recommendations_input)
        self.assertFalse(result.is_success)
        self.assertEqual('123', result.errors.deep_errors[0].code)
        self.assertEqual('Error 1', result.errors.deep_errors[0].message)


