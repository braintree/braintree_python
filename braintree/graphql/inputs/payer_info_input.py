from typing import Dict, Optional
from braintree.graphql.inputs.billing_address_input import BillingAddressInput
from braintree.graphql.inputs.shipping_address_input import ShippingAddressInput

class PayerInfoInput:
    """
    Represents payer information for a local payment.
    """

    def __init__(
        self,
        billing_address: Optional[dict] = None,
        email: Optional[str] = None,
        given_name: Optional[str] = None,
        phone_country_code: Optional[str] = None,
        phone_number: Optional[str] = None,
        shipping_address: Optional[dict] = None,
        surname: Optional[str] = None
    ):
        self._billing_address = BillingAddressInput(**billing_address) if billing_address else None
        self._email = email
        self._given_name = given_name
        self._phone_country_code = phone_country_code
        self._phone_number = phone_number
        self._shipping_address = ShippingAddressInput(**shipping_address) if shipping_address else None
        self._surname = surname

    def to_graphql_variables(self) -> Dict:
        """
        Returns a dictionary representing the input object, to pass as variables to a GraphQL mutation.
        """
        variables = {}
        if self._billing_address is not None:
            variables["billingAddress"] = self._billing_address.to_graphql_variables()
        if self._email is not None:
            variables["email"] = self._email
        if self._given_name is not None:
            variables["givenName"] = self._given_name
        if self._phone_country_code is not None:
            variables["phoneCountryCode"] = self._phone_country_code
        if self._phone_number is not None:
            variables["phoneNumber"] = self._phone_number
        if self._shipping_address is not None:
            variables["shippingAddress"] = self._shipping_address.to_graphql_variables()
        if self._surname is not None:
            variables["surname"] = self._surname

        return variables
