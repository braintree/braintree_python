from typing import Dict, Optional

class ShippingAddressInput:
    """
    Represents shipping address information for a payer.
    """

    def __init__(
        self,
        country_code_alpha2: Optional[str] = None,
        extended_address: Optional[str] = None,
        locality: Optional[str] = None,
        postal_code: Optional[str] = None,
        region: Optional[str] = None,
        street_address: Optional[str] = None
    ):
        self._country_code_alpha2 = country_code_alpha2
        self._extended_address = extended_address
        self._locality = locality
        self._postal_code = postal_code
        self._region = region
        self._street_address = street_address

    def to_graphql_variables(self) -> Dict:
        """
        Returns a dictionary representing the input object, to pass as variables to a GraphQL mutation.
        """
        variables = {}
        if self._country_code_alpha2 is not None:
            variables["countryCode"] = self._country_code_alpha2
        if self._extended_address is not None:
            variables["extendedAddress"] = self._extended_address
        if self._locality is not None:
            variables["locality"] = self._locality
        if self._postal_code is not None:
            variables["postalCode"] = self._postal_code
        if self._region is not None:
            variables["region"] = self._region
        if self._street_address is not None:
            variables["streetAddress"] = self._street_address

        return variables
