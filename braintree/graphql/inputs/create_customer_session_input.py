from typing import Dict
from braintree.graphql.inputs.customer_session_input import CustomerSessionInput


class CreateCustomerSessionInput:
    """
    Represents the input to request the creation of a PayPal customer session.
    """

    def __init__(
        self,
        merchant_account_id: str = None,
        session_id: str = None,
        customer: CustomerSessionInput = None,
        domain: str = None,
    ):
        self._merchant_account_id = merchant_account_id
        self._session_id = session_id
        self._customer = customer
        self._domain = domain

    def to_graphql_variables(self) -> Dict:
        variables = {}
        if self._merchant_account_id is not None:
            variables["merchantAccountId"] = self._merchant_account_id
        if self._session_id is not None:
            variables["sessionId"] = self._session_id
        if self._customer is not None:
            variables["customer"] = self._customer.to_graphql_variables()
        if self._domain is not None:
            variables["domain"] = self._domain
        return variables

    @staticmethod
    def builder():
        """
        Creates a builder instance for fluent construction of CreateCustomerSessionInput objects.
        """
        return CreateCustomerSessionInput.Builder()

    class Builder:
        def __init__(self):
            self._merchant_account_id = None
            self._session_id = None
            self._customer = None
            self._domain = None

        def merchant_account_id(self, merchant_account_id: str):
            """
            Sets the merchant account ID.
            """
            self._merchant_account_id = merchant_account_id
            return self

        def session_id(self, session_id: str):
            """
            Sets the customer session ID.
            """
            self._session_id = session_id
            return self

        def customer(self, customer: str):
            """
            Sets the input object representing customer information relevant to the customer session.
            """
            self._customer = customer
            return self

        def domain(self, domain: str):
            """
            Sets the customer domain.
            """
            self._domain = domain
            return self

        def build(self):
            return CreateCustomerSessionInput(
                self._merchant_account_id,
                self._session_id,
                self._customer,
                self._domain,
            )
