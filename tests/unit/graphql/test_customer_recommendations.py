from tests.test_helper import unittest
from braintree.graphql.enums.recommended_payment_option import RecommendedPaymentOption
from braintree.graphql.types.payment_recommendation import PaymentRecommendation
from braintree.graphql.types.payment_options import PaymentOptions
from braintree.graphql.unions.customer_recommendations import CustomerRecommendations

class TestCustomerRecommendations(unittest.TestCase):
    def test_init_with_payment_recommendations(self):
        rec1 = PaymentRecommendation(RecommendedPaymentOption.PAYPAL, 1)
        rec2 = PaymentRecommendation(RecommendedPaymentOption.VENMO, 2)
        recommendations = [rec1, rec2]

        customer_recs = CustomerRecommendations(payment_recommendations=recommendations)

        self.assertEqual(customer_recs.payment_recommendations, recommendations)

    def test_init_with_none(self):
        customer_recs = CustomerRecommendations()
        self.assertEqual(customer_recs.payment_recommendations, [])
    
    def test_payment_options_extracted(self):
        rec1 = PaymentRecommendation(RecommendedPaymentOption.PAYPAL, 1)
        rec2 = PaymentRecommendation(RecommendedPaymentOption.VENMO, 2)
        recommendations = [rec1, rec2]

        customer_recs = CustomerRecommendations(payment_recommendations=recommendations)

        expected_payment_options = [
            PaymentOptions(RecommendedPaymentOption.PAYPAL, 1),
            PaymentOptions(RecommendedPaymentOption.VENMO, 2)
        ]

        self.assertEqual(customer_recs.payment_options[0].payment_option, expected_payment_options[0].payment_option) 
        self.assertEqual(customer_recs.payment_options[0].recommended_priority, expected_payment_options[0].recommended_priority) 
        self.assertEqual(customer_recs.payment_options[1].payment_option, expected_payment_options[1].payment_option) 
        self.assertEqual(customer_recs.payment_options[1].recommended_priority, expected_payment_options[1].recommended_priority) 
