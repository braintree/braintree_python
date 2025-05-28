import unittest
import braintree
from braintree import (
    CreateCustomerSessionInput, 
    CustomerSessionInput, 
    PhoneInput, 
    UpdateCustomerSessionInput, 
    CustomerRecommendationsInput, 
    Recommendations,
    PayPalPurchaseUnitInput,
    MonetaryAmountInput
)
from braintree.graphql.enums.recommended_payment_option import RecommendedPaymentOption
from braintree.exceptions.authorization_error import AuthorizationError
from braintree.util.graphql_client import GraphQLClient
from decimal import Decimal 
import json 

class CustomerSessionIT(unittest.TestCase):

    def test_create_customer_session_without_email_and_phone(self):
        input = (
            CreateCustomerSessionInput
            .builder()
            .merchant_account_id("usd_pwpp_multi_account_merchant_account")
            .build()
        )

        result = self.pwpp_gateway().customer_session.create_customer_session(input)
        self.assertIsNotNone(result.session_id)

    def test_create_customer_session_with_merchant_provided_session_id(self):
        merchant_session_id = "11EF-A1E7-A5F5EE5C-A2E5-AFD2801469FC"
        input = (
            CreateCustomerSessionInput
            .builder()
            .session_id(merchant_session_id)
            .build()
        )

        result = self.pwpp_gateway().customer_session.create_customer_session(input)
        self.assertEqual(merchant_session_id, result.session_id)

    def test_create_customer_session_with_api_derived_session_id(self):
        result = self.build_customer_session(None)
        self.assertIsNotNone(result.session_id)

    def test_create_customer_session_with_purchase_units(self):
        input = (
            CreateCustomerSessionInput
            .builder()
            .purchase_units(self.build_purchase_units())
            .build()
        )

        result = self.pwpp_gateway().customer_session.create_customer_session(input)
        self.assertTrue(result.is_success)
        self.assertIsNotNone(result.session_id)

    def test_does_not_create_duplicate_customer_session(self):
        existing_session_id = "11EF-34BC-2702904B-9026-C3ECF4BAC765"

        result = self.build_customer_session(existing_session_id)

        self.assertFalse(result.is_success)
        self.assertIn("Session IDs must be unique per merchant", result.errors.deep_errors[0].message)

    def test_update_customer_session(self):
        session_id = "11EF-A1E7-A5F5EE5C-A2E5-AFD2801469FC"
        create_input = (
            CreateCustomerSessionInput
            .builder()
            .session_id(session_id)
            .merchant_account_id("usd_pwpp_multi_account_merchant_account")
            .purchase_units(self.build_purchase_units())
            .build()
        )
        self.pwpp_gateway().customer_session.create_customer_session(create_input)

        customer = self.build_customer_session_input()
        input = (
            UpdateCustomerSessionInput
            .builder(session_id)
            .customer(customer)
            .build()
        )

        result = self.pwpp_gateway().customer_session.update_customer_session(input)

        self.assertTrue(result.is_success)
        self.assertEqual(session_id, result.session_id)

    def test_does_not_update_non_existent_session(self):
        session_id = "11EF-34BC-2702904B-9026-C3ECF4BAC765"
        customer = self.build_customer_session_input()
        input = (
            UpdateCustomerSessionInput
            .builder(session_id)
            .customer(customer)
            .build()
        )

        result = self.pwpp_gateway().customer_session.update_customer_session(input)
        self.assertFalse(result.is_success)
        self.assertIn("does not exist", result.errors.deep_errors[0].message)

    def test_get_customer_recommendations(self):
        customer = self.build_customer_session_input()
        recommendation = Recommendations.PAYMENT_RECOMMENDATIONS
        recommendationsList: List[Recommendations] = []
        recommendationsList.append(recommendation)
        customer_recommendations_input = (
            CustomerRecommendationsInput
            .builder()
            .session_id("94f0b2db-5323-4d86-add3-paypal000000")
            .customer(customer)
            .purchase_units(self.build_purchase_units())
            .domain("domain.com")
            .build()
        )
        
        result = self.pwpp_gateway().customer_session.get_customer_recommendations(customer_recommendations_input)
        self.assertTrue(result.is_success)
        payload = result.customer_recommendations
        
        self.assertTrue(payload.is_in_paypal_network)
        
        recommendation = payload.recommendations.payment_recommendations[0]
        self.assertEqual(RecommendedPaymentOption.PAYPAL, recommendation.payment_option)
        self.assertEqual(1, recommendation.recommended_priority)

    def test_does_not_get_recommendations_when_not_authorized(self):
        customer = (
            CustomerSessionInput
            .builder()
            .device_fingerprint_id("00DD010662DE")
            .user_agent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/x.x.x.x Safari/537.36")
            .build()
        )
        recommendation = Recommendations.PAYMENT_RECOMMENDATIONS
        recommendationsList: List[Recommendations] = []
        recommendationsList.append(recommendation)
        customer_recommendations_input = (
            CustomerRecommendationsInput
            .builder()
            .session_id("6B29FC40-CA47-1067-B31D-00DD010662DA")
            .customer(customer)
            .purchase_units(self.build_purchase_units())
            .domain("domain.com")
            .merchant_account_id("gbp_pwpp_multi_account_merchant_account")
            .build()
        )

        with self.assertRaises(AuthorizationError):
            self.pwpp_gateway().customer_session.get_customer_recommendations(customer_recommendations_input)
    
    def pwpp_gateway(self):
        return braintree.BraintreeGateway(
            braintree.Configuration(
                environment=braintree.Environment.Development,
                merchant_id="pwpp_multi_account_merchant",
                public_key="pwpp_multi_account_merchant_public_key",
                private_key="pwpp_multi_account_merchant_private_key"
            )
        )

    def build_customer_session(self, session_id):
        customer = self.build_customer_session_input()
        input_builder = (
            CreateCustomerSessionInput
            .builder()
            .customer(customer)
        )
        
        if session_id:
            input_builder = input_builder.session_id(session_id)

        return self.pwpp_gateway().customer_session.create_customer_session(input_builder.build())

    def build_customer_session_input(self):
        phone = (
            PhoneInput
            .builder()
            .country_phone_code("1")
            .phone_number("4088888888")
            .build()
        )

        return (
            CustomerSessionInput
            .builder()
            .hashed_email("48ddb93f0b30c475423fe177832912c5bcdce3cc72872f8051627967ef278e08")
            .hashed_phone_number("a2df2987b2a3384210d3aa1c9fb8b627ebdae1f5a9097766c19ca30ec4360176")
            .device_fingerprint_id("00DD010662DE")
            .user_agent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/x.x.x.x Safari/537.36")
            .build()
        )
        
    def build_purchase_units(self):
        amount = MonetaryAmountInput(currency_code="USD", value=Decimal("10.00"))
        purchase_units = []
        purchase_unit = PayPalPurchaseUnitInput.builder(amount).build()
        purchase_units.append(purchase_unit)

        return purchase_units
