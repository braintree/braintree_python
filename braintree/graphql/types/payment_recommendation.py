from braintree.graphql.enums import RecommendedPaymentOption
from braintree.util.experimental import Experimental

@Experimental
# This class is Experiemental and may change in future releases.
class PaymentRecommendation:
    """
    Represents a single  payment method and priority associated with a PayPal customer session.
    """

    def __init__(self, payment_option: RecommendedPaymentOption, recommended_priority: int):
        self.payment_option = payment_option
        self.recommended_priority = recommended_priority
