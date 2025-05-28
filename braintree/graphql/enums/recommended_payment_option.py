from enum import Enum
from braintree.util.experimental import Experimental


@Experimental
# This enum is Experiemental and may change in future releases.
class RecommendedPaymentOption(Enum):
    """
    Represents available payment options related to PayPal customer session recommendations.
    """

    PAYPAL = "PAYPAL"
    VENMO = "VENMO"
