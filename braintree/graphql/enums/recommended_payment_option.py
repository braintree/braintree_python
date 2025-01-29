from enum import Enum


class RecommendedPaymentOption(Enum):
    """
    Represents available payment options related to PayPal customer session recommendations.
    """

    PAYPAL = "PAYPAL"
    VENMO = "VENMO"
