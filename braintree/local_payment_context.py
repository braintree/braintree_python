from braintree.attribute_getter import AttributeGetter
from braintree.monetary_amount import MonetaryAmount

class LocalPaymentContext(AttributeGetter):
    """
    Represents a local payment context.
    """

    @staticmethod
    def _extract_amount(response):
        """Extract and construct MonetaryAmount from response"""
        amount_hash = LocalPaymentContext._get_value_optional(response, "paymentContext.amount")
        if not amount_hash:
            return None

        currency = (amount_hash.get("currencyCode") or
                   amount_hash.get("currencyIsoCode"))

        return MonetaryAmount({
            "value": amount_hash.get("value"),
            "currency_code": currency
        })

    @staticmethod
    def _get_value(response, key):
        """Get a value from nested response dictionary"""
        current_map = response
        key_parts = key.split(".")

        for i in range(len(key_parts) - 1):
            sub_key = key_parts[i]
            current_map = LocalPaymentContext._pop_value(current_map, sub_key)

        last_key = key_parts[-1]
        return LocalPaymentContext._pop_value(current_map, last_key)

    @staticmethod
    def _get_value_optional(response, key):
        """Get an optional value from nested response dictionary"""
        try:
            return LocalPaymentContext._get_value(response, key)
        except (KeyError, TypeError):
            return None

    @staticmethod
    def _pop_value(response, key):
        """Pop a value from dictionary, trying both string and symbol keys"""
        if key in response:
            return response[key]

        if response.get(key):
            return response.get(key)

        raise KeyError("Couldn't parse response - missing key: {0}".format(key))

    def __init__(self, attributes=None):
        if attributes is None:
            attributes = {}

        if "response" in attributes:
            response = attributes["response"]
            processed_attrs = {
                "id": self._get_value(response, "paymentContext.id"),
                "legacy_id": self._get_value_optional(response, "paymentContext.legacyId"),
                "type": self._get_value(response, "paymentContext.type"),
                "payment_id": self._get_value_optional(response, "paymentContext.paymentId"),
                "order_id": self._get_value_optional(response, "paymentContext.orderId"),
                "approval_url": self._get_value_optional(response, "paymentContext.approvalUrl"),
                "merchant_account_id": self._get_value_optional(response, "paymentContext.merchantAccountId"),
                "created_at": self._get_value_optional(response, "paymentContext.createdAt"),
                "updated_at": self._get_value_optional(response, "paymentContext.updatedAt"),
                "transacted_at": self._get_value_optional(response, "paymentContext.transactedAt"),
                "approved_at": self._get_value_optional(response, "paymentContext.approvedAt"),
                "expired_at": self._get_value_optional(response, "paymentContext.expiredAt"),
                "amount": self._extract_amount(response)
            }
            AttributeGetter.__init__(self, processed_attrs)
        else:
            AttributeGetter.__init__(self, attributes)

    def __repr__(self):
        detail_list = [
            "id",
            "legacy_id",
            "type",
            "payment_id",
            "order_id",
            "approval_url",
            "merchant_account_id",
            "created_at",
            "updated_at",
            "transacted_at",
            "approved_at",
            "expired_at",
            "amount"
        ]
        return super(LocalPaymentContext, self).__repr__(detail_list)
