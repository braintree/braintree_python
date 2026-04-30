from typing import Dict, Optional
from braintree.graphql.inputs.monetary_amount_input import MonetaryAmountInput
from braintree.graphql.inputs.payer_info_input import PayerInfoInput

class CreateLocalPaymentContextInput:
    """
    Represents input for creating a local payment context.
    """

    def __init__(
        self,
        amount: Optional[dict] = None,
        cancel_url: Optional[str] = None,
        country_code: Optional[str] = None,
        expiry_date: Optional[str] = None,
        merchant_account_id: Optional[str] = None,
        order_id: Optional[str] = None,
        payer_info: Optional[dict] = None,
        return_url: Optional[str] = None,
        type: Optional[str] = None
    ):
        self._amount = MonetaryAmountInput(**amount) if amount else None
        self._cancel_url = cancel_url
        self._country_code = country_code
        self._expiry_date = expiry_date
        self._merchant_account_id = merchant_account_id
        self._order_id = order_id
        self._payer_info = PayerInfoInput(**payer_info) if payer_info else None
        self._return_url = return_url
        self._type = type

    def to_graphql_variables(self) -> Dict:
        """
        Returns a dictionary representing the input object, to pass as variables to a GraphQL mutation.
        """
        payment_context = {}
        if self._amount is not None:
            payment_context["amount"] = self._amount.to_graphql_variables()
        if self._cancel_url is not None:
            payment_context["cancelUrl"] = self._cancel_url
        if self._country_code is not None:
            payment_context["countryCode"] = self._country_code
        if self._expiry_date is not None:
            payment_context["expiryDate"] = self._expiry_date
        if self._merchant_account_id is not None:
            payment_context["merchantAccountId"] = self._merchant_account_id
        if self._order_id is not None:
            payment_context["orderId"] = self._order_id
        if self._payer_info is not None:
            payment_context["payerInfo"] = self._payer_info.to_graphql_variables()
        if self._return_url is not None:
            payment_context["returnUrl"] = self._return_url
        if self._type is not None:
            payment_context["type"] = self._type

        return {"paymentContext": payment_context}
