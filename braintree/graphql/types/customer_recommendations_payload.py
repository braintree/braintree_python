from braintree.graphql.unions.customer_recommendations import CustomerRecommendations


class CustomerRecommendationsPayload:
    """
    Represents the customer recommendations information associated with a PayPal customer session.
    """

    def __init__(self, is_in_paypal_network: bool, recommendations: CustomerRecommendations):
        self.is_in_paypal_network = is_in_paypal_network
        self.recommendations = recommendations
