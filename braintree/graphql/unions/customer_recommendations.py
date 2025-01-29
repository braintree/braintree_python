from typing import List
from braintree.graphql.types.payment_options import PaymentOptions


class CustomerRecommendations:
    """
    A union of all possible customer recommendations associated with a PayPal customer session.
    """

    def __init__(self, payment_options: List[PaymentOptions]):
        self.payment_options = payment_options
