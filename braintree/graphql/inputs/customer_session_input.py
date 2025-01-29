from typing import Dict

from braintree.graphql.inputs.phone_input import PhoneInput


class CustomerSessionInput:
    """
    Customer identifying information for a PayPal customer session.
    """

    def __init__(
        self,
        email: str = None,
        phone: PhoneInput = None,
        device_fingerprint_id: str = None,
        paypal_app_installed: bool = None,
        venmo_app_installed: bool = None,
        user_agent: str = None,
    ):
        self._email = email
        self._phone = phone
        self._device_fingerprint_id = device_fingerprint_id
        self._paypal_app_installed = paypal_app_installed
        self._venmo_app_installed = venmo_app_installed
        self._user_agent = user_agent

    def to_graphql_variables(self) -> Dict:
        variables = {}
        if self._email is not None:
            variables["email"] = self._email
        if self._device_fingerprint_id is not None:
            variables["deviceFingerprintId"] = self._device_fingerprint_id
        if self._phone is not None:
            variables["phone"] = self._phone.to_graphql_variables()
        if self._paypal_app_installed is not None:
            variables["paypalAppInstalled"] = self._paypal_app_installed
        if self._venmo_app_installed is not None:
            variables["venmoAppInstalled"] = self._venmo_app_installed
        if self._user_agent is not None:
            variables["userAgent"] = self._user_agent

        return variables

    @staticmethod
    def builder():
        """
        Creates a builder instance for fluent construction of CustomerSessionInput objects.
        """
        return CustomerSessionInput.Builder()

    class Builder:
        def __init__(self):
            self._email = None
            self._phone = None
            self._device_fingerprint_id = None
            self._paypal_app_installed = None
            self._venmo_app_installed = None
            self._user_agent = None

        def email(self, email: str):
            """
            Sets the customer email address.
            """
            self._email = email
            return self

        def phone(self, phone: PhoneInput):
            """
            Sets the customer phone number input object.
            """
            self._phone = phone
            return self

        def device_fingerprint_id(self, device_fingerprint_id: str):
            """
            Sets the device fingerprint ID.
            """
            self._device_fingerprint_id = device_fingerprint_id
            return self

        def paypal_app_installed(self, paypal_app_installed: bool):
            """
            Sets whether the PayPal app is installed on the customer's device.
            """
            self._paypal_app_installed = paypal_app_installed
            return self

        def venmo_app_installed(self, venmo_app_installed: bool):
            """
            Sets whether the Venmo app is installed on the customer's device.
            """
            self._venmo_app_installed = venmo_app_installed
            return self

        def user_agent(self, user_agent: str):
            """
            Sets user agent from the request originating from the customer's device.
            This will be used to identify the customer's operating system and browser versions.
            """
            self._user_agent = user_agent
            return self

        def build(self):
            return CustomerSessionInput(
                self._email,
                self._phone,
                self._device_fingerprint_id,
                self._paypal_app_installed,
                self._venmo_app_installed,
                self._user_agent,
            )
