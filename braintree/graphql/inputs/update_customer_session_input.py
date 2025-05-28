from typing import Dict, List
from braintree.graphql.inputs.customer_session_input import CustomerSessionInput
from braintree.graphql.inputs.paypal_purchase_unit_input import PayPalPurchaseUnitInput
from braintree.util.experimental import Experimental

@Experimental
# This class is Experiemental and may change in future releases.
class UpdateCustomerSessionInput:
    """
    Represents the input to request an update to a PayPal customer session.
    """

    def __init__(
        self,
        session_id: str,
        customer: CustomerSessionInput = None,
        merchant_account_id: str = None,
        purchase_units: List[PayPalPurchaseUnitInput] = None, 
    ):
        self._session_id = session_id
        self._customer = customer
        self._merchant_account_id = merchant_account_id
        self._purchase_units = purchase_units 

    def to_graphql_variables(self) -> Dict:
        variables = {}
        if self._session_id:
            variables["sessionId"] = self._session_id
        if self._customer:
            variables["customer"] = self._customer.to_graphql_variables()
        if self._merchant_account_id:
            variables["merchantAccountId"] = self._merchant_account_id
        if self._purchase_units is not None:
            variables["purchaseUnits"] = [
                purchase_unit.to_graphql_variables()
                for purchase_unit in self._purchase_units
            ]
        return variables

    @staticmethod
    def builder(session_id: str):
        """
        Creates a builder instance for fluent construction of UpdateCustomerSessionInput objects.

        Args:
            session_id (str): ID of the customer session to be updated.
        """
        return UpdateCustomerSessionInput.Builder(session_id)

    class Builder:
        def __init__(self, session_id: str):
            self._session_id = session_id
            self._customer = None
            self._merchant_account_id = None
            self._purchase_units = None 

        def merchant_account_id(self, merchant_account_id: str):
            """
            Sets the merchant account ID.
            """
            self._merchant_account_id = merchant_account_id
            return self

        def customer(self, customer: CustomerSessionInput):
            """
            Sets the input object representing customer information relevant to the customer session.
            """
            self._customer = customer
            return self
        
        def purchase_units(self, purchase_units: List[PayPalPurchaseUnitInput]):
            """
            Sets the Purchase Units for the items purchased.
            """
            self._purchase_units = purchase_units
            return self

        def build(self):
            return UpdateCustomerSessionInput(
                self._session_id,
                self._customer,
                self._merchant_account_id,
                self._purchase_units
            )
