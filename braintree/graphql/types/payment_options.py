from braintree.graphql.enums import RecommendedPaymentOption


class PaymentOptions:
    """
    Represents the payment method and priority associated with a PayPal customer session.
    """

    def __init__(self, payment_option: RecommendedPaymentOption, recommended_priority: int):
        self.payment_option = payment_option
        self.recommended_priority = recommended_priority
