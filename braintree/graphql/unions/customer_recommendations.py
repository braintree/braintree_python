from typing import List, Optional
from braintree.graphql.types.payment_options import PaymentOptions
from braintree.graphql.types.payment_recommendation import PaymentRecommendation
from braintree.util.experimental import Experimental

@Experimental
# This class is Experiemental and may change in future releases.
class CustomerRecommendations:
    """
    A union of all possible customer recommendations associated with a PayPal customer session.
    """

    def __init__(
        self, 
        payment_recommendations: Optional[List[PaymentRecommendation]] = None
    ):
        """
        Initialize customer recommendations.
        
        Args:
            payment_recommendations: A list of PaymentRecommendation objects
        """
        # Initialize payment_options
        self.payment_options = []
        
        # Initialize payment_recommendations
        if payment_recommendations is not None:
            self.payment_recommendations = payment_recommendations

            self.payment_options = [
                PaymentOptions(
                    recommendation.payment_option,
                    recommendation.recommended_priority
                )
                for recommendation in payment_recommendations
            ]
        else:
            self.payment_recommendations = []
