from typing import List, Dict
from braintree.graphql.inputs.customer_session_input import CustomerSessionInput
from braintree.graphql.inputs.paypal_purchase_unit_input import PayPalPurchaseUnitInput
from braintree.graphql.enums.recommendations import Recommendations
from braintree.util.experimental import Experimental

@Experimental
# This class is Experiemental and may change in future releases.
class CustomerRecommendationsInput:
    """
    Represents the input to request PayPal customer session recommendations.
    """

    def __init__(
        self,
        session_id: str,
        merchant_account_id: str = None,
        purchase_units: List[PayPalPurchaseUnitInput] = None, 
        domain: str = None,
        customer: CustomerSessionInput = None,
    ):

        self._session_id = session_id
        self._merchant_account_id = merchant_account_id
        self._purchase_units = purchase_units
        self._domain = domain 
        self._customer = customer

    def to_graphql_variables(self) -> Dict:
        variables = {
            "sessionId": self._session_id
        }
        if self._merchant_account_id is not None:
            variables["merchantAccountId"] = self._merchant_account_id
        if self._purchase_units is not None:
            variables["purchaseUnits"] = [
                purchase_unit.to_graphql_variables()
                for purchase_unit in self._purchase_units
            ]
        if self._domain is not None: 
            variables["domain"] = self._domain 
        if self._customer is not None:
            variables["customer"] = self._customer.to_graphql_variables()

        return variables

    @staticmethod
    def builder():
        """
        Creates a builder instance for fluent construction of CustomerRecommendationsInput objects.
        """
        return CustomerRecommendationsInput.Builder()

    class Builder:
        def __init__(self):
            self._session_id = None
            self._merchant_account_id = None
            self._purchase_units = None
            self._domain = None 
            self._customer = None

        def session_id(self, session_id: str):
            """
            Sets the ID of the customer session to access customer session information.
            """
            self._session_id = session_id
            return self

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

        def domain(self, domain: str):
            """
            Sets the customer domain.
            """
            self._domain = domain
            return self

        def build(self):
            return CustomerRecommendationsInput(
                self._session_id,
                self._merchant_account_id,
                self._purchase_units,
                self._domain,
                self._customer, 
            )
