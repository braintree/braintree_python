from enum import Enum
from braintree.util.experimental import Experimental

@Experimental
# This enum is Experiemental and may change in future releases.
class Recommendations(Enum):
    """
    Represents available types of customer recommendations that can be retrieved using a PayPal customer session.
    """

    PAYMENT_RECOMMENDATIONS = "PAYMENT_RECOMMENDATIONS"
