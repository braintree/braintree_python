class PhoneInput:
    """
    Phone number input for PayPal customer session.
    """

    def __init__(
        self,
        country_phone_code: str = None,
        phone_number: str = None,
        extension_number: str = None
    ):
        self._country_phone_code = country_phone_code
        self._phone_number = phone_number
        self._extension_number = extension_number

    def to_graphql_variables(self):
        variables = {}
        if self._country_phone_code is not None:
            variables["countryPhoneCode"] = self._country_phone_code
        if self._phone_number is not None:
            variables["phoneNumber"] = self._phone_number
        if self._extension_number is not None:
            variables["extensionNumber"] = self._extension_number
        return variables

    @staticmethod
    def builder():
        """
        Creates a builder instance for fluent construction of PhoneInput objects.
        """
        return PhoneInput.Builder()

    class Builder:
        def __init__(self):
            self._country_phone_code = None
            self._phone_number = None
            self._extension_number = None

        def country_phone_code(self, country_phone_code: str):
            """
            Sets the country phone code for the phone number.
            """
            self._country_phone_code = country_phone_code
            return self

        def phone_number(self, phone_number: str):
            """
            Sets the phone number.
            """
            self._phone_number = phone_number
            return self

        def extension_number(self, extension_number: str):
            """
            Sets the extension number.
            """
            self._extension_number = extension_number
            return self

        def build(self):
            return PhoneInput(
                self._country_phone_code, self._phone_number, self._extension_number
            )
