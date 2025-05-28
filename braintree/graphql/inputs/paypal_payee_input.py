from typing import Dict
from braintree.util.experimental import Experimental

@Experimental
# This class is Experiemental and may change in future releases.
class PayPalPayeeInput:
    """
    The details for the merchant who receives the funds and fulfills the order.
    The merchant is also known as the payee.
    """

    def __init__(
        self,
        email_address: str = None,
        client_id: str = None,
    ):
        self._email_address = email_address
        self._client_id = client_id

    def to_graphql_variables(self) -> Dict:
        """
        Returns a dictionary representing the input object, to pass as variables to a GraphQL mutation.
        """
        variables = {}
        if self._email_address is not None:
            variables["emailAddress"] = self._email_address
        if self._client_id is not None:
            variables["clientId"] = self._client_id
        return variables

    @staticmethod
    def builder():
        """
        Creates a builder instance for fluent construction of PayPalPayeeInput objects.
        """
        return PayPalPayeeInput.Builder()

    class Builder:
        def __init__(self):
            self._email_address = None
            self._client_id = None

        def email_address(self, email_address: str):
            """
            Sets the email address of this merchant.
            """
            self._email_address = email_address
            return self

        def client_id(self, client_id: str):
            """
            Sets the public ID for the payee- or merchant-created app.
            """
            self._client_id = client_id
            return self

        def build(self):
            return PayPalPayeeInput(
                self._email_address, self._client_id
            )
