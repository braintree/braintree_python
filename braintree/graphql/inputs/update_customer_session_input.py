from typing import Dict
from braintree.graphql.inputs.customer_session_input import CustomerSessionInput


class UpdateCustomerSessionInput:
    """
    Represents the input to request an update to a PayPal customer session.
    """

    def __init__(
        self,
        session_id: str,
        merchant_account_id: str = None,
        customer: CustomerSessionInput = None,
    ):
        self._session_id = session_id
        self._merchant_account_id = merchant_account_id
        self._customer = customer

    def to_graphql_variables(self) -> Dict:
        variables = {}
        if self._session_id:
            variables["sessionId"] = self._session_id
        if self._merchant_account_id:
            variables["merchantAccountId"] = self._merchant_account_id
        if self._customer:
            variables["customer"] = self._customer.to_graphql_variables()
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
            self._merchant_account_id = None
            self._customer = None

        def merchant_account_id(self, merchant_account_id):
            """
            Sets the merchant account ID.
            """
            self._merchant_account_id = merchant_account_id
            return self

        def customer(self, customer):
            """
            Sets the input object representing customer information relevant to the customer session.
            """
            self._customer = customer
            return self

        def build(self):
            return UpdateCustomerSessionInput(
                self._session_id,
                self._merchant_account_id,
                self._customer
            )
