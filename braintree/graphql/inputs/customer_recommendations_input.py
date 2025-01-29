from typing import List, Dict
from braintree.graphql.inputs.customer_session_input import CustomerSessionInput
from braintree.graphql.enums.recommendations import Recommendations


class CustomerRecommendationsInput:
    """
    Represents the input to request PayPal customer session recommendations.
    """

    def __init__(
        self,
        session_id: str,
        recommendations: List[Recommendations],
        merchant_account_id: str = None,
        customer: CustomerSessionInput = None,
    ):
        self._session_id = session_id
        self._recommendations = recommendations
        self._merchant_account_id = merchant_account_id
        self._customer = customer

    def to_graphql_variables(self) -> Dict:
        variables = {
            "sessionId": self._session_id,
            "recommendations": [recommendation.name for recommendation in self._recommendations],
        }
        if self._merchant_account_id is not None:
            variables["merchantAccountId"] = self._merchant_account_id
        if self._customer is not None:
            variables["customer"] = (
                self._customer.to_graphql_variables()
                if hasattr(self._customer, "to_graphql_variables")
                else self._customer
            )
        return variables

    @staticmethod
    def builder(session_id: str, recommendations: List[Recommendations]):
        """
        Creates a builder instance for fluent construction of CustomerRecommendationsInput objects.

        Args:
            session_id (str): ID of the customer session for getting recommendations.
            recommendations (List[Recommendations]): List of recommendations to retrieve for the customer session.
        """
        return CustomerRecommendationsInput.Builder(session_id, recommendations)

    class Builder:
        def __init__(self, session_id: str, recommendations: List[Recommendations]):
            self._session_id = session_id
            self._recommendations = recommendations
            self._merchant_account_id = None
            self._customer = None

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

        def build(self):
            return CustomerRecommendationsInput(
                self._session_id,
                self._recommendations,
                self._merchant_account_id,
                self._customer,
            )
