import unittest
import braintree
from braintree import CreateCustomerSessionInput, CustomerSessionInput, PhoneInput, UpdateCustomerSessionInput, CustomerRecommendationsInput, Recommendations
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
            .build()
        )
        self.pwpp_gateway().customer_session.create_customer_session(create_input)

        customer = self.build_customer_session_input("PR5_test@example.com", "4085005005")
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
        customer = self.build_customer_session_input("PR9_test@example.com", "4085005009")
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
        customer = self.build_customer_session_input("PR5_test@example.com", "4085005005");
        customer_recommendations_input = (
                CustomerRecommendationsInput
                    .builder("11EF-A1E7-A5F5EE5C-A2E5-AFD2801469FC", [Recommendations.PAYMENT_RECOMMENDATIONS])
                    .customer(customer)
                    .build()
            )
        
        result = self.pwpp_gateway().customer_session.get_customer_recommendations(customer_recommendations_input)
        self.assertTrue(result.is_success)
        self.assertTrue(result.customer_recommendations.is_in_paypal_network)
        payment_options = result.customer_recommendations.recommendations.payment_options
        self.assertEqual(1, len(payment_options))
        self.assertEqual("PAYPAL", payment_options[0].payment_option)
        self.assertEqual(1, payment_options[0].recommended_priority)

    def test_does_not_get_customer_recommendations_for_non_existent_session(self):
        customer = self.build_customer_session_input("PR9_test@example.com", "4085005009");
        customer_recommendations_input = (
                CustomerRecommendationsInput
                    .builder("11EF-34BC-2702904B-9026-C3ECF4BAC765", [Recommendations.PAYMENT_RECOMMENDATIONS])
                    .customer(customer)
                    .build()
            )
        
        result = self.pwpp_gateway().customer_session.get_customer_recommendations(customer_recommendations_input)
        self.assertFalse(result.is_success)
        self.assertIn("does not exist", result.errors.deep_errors[0].message)




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
        customer = self.build_customer_session_input("PR1_test@example.com", "4085005002")
        input_builder = (CreateCustomerSessionInput
            .builder()
            .customer(customer)
        )
        if session_id:
            input_builder = input_builder.session_id(session_id)

        return self.pwpp_gateway().customer_session.create_customer_session(input_builder.build())


    def build_customer_session_input(self, email, phone_number):
        phone = (
            PhoneInput
                .builder()
                .country_phone_code("1")
                .phone_number(phone_number)
                .build()
        )

        return (
            CustomerSessionInput
                .builder()
                .email(email)
                .device_fingerprint_id("test")
                .phone(phone)
                .paypal_app_installed(True)
                .venmo_app_installed(True)
                .user_agent("Mozilla")
                .build()
        )
