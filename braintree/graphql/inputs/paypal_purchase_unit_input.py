from typing import Dict
from braintree.graphql.inputs.monetary_amount_input import MonetaryAmountInput 
from braintree.graphql.inputs.paypal_payee_input import PayPalPayeeInput
from braintree.util.experimental import Experimental


@Experimental
class PayPalPurchaseUnitInput: 
    """
    Payee and Amount of the item purchased.
    """

    def __init__(
        self, 
        amount: MonetaryAmountInput = None, 
        payee: PayPalPayeeInput = None
    ):

        self._amount = amount 
        self._payee = payee

    def to_graphql_variables(self) -> Dict:
        """
        Returns a dictionary representing the input object, to pass as variables to a GraphQL mutation.
        """
        variables = {}
        if self._payee is not None:
            variables["payee"] = self._payee.to_graphql_variables()
        if self._amount is not None:
            variables["amount"] = self._amount.to_graphql_variables()
        return variables 

    @staticmethod
    def builder(amount: MonetaryAmountInput):
        """
        Creates a builder instance for fluent construction of PayPalPurchaseUnit objects.

        Args:
        amount (MonetaryAmountInput): The total order amount. The amount must be a positive number.

        """
        return PayPalPurchaseUnitInput.Builder(amount)

    class Builder:
        def __init__(self, amount: MonetaryAmountInput):
            self._amount = amount
            self._payee = None
            
        def payee(self, payee: PayPalPayeeInput):
            """
            Sets the PayPal payee.
            """
            self._payee = payee
            return self

        def build(self):
            return PayPalPurchaseUnitInput(
                self._amount,
                self._payee
            )