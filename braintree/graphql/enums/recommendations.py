from enum import Enum


class Recommendations(Enum):
    """
    Represents available types of customer recommendations that can be retrieved using a PayPal customer session.
    """

    PAYMENT_RECOMMENDATIONS = "PAYMENT_RECOMMENDATIONS"
