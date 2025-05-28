from decimal import Decimal 
from typing import Dict
from braintree.util.experimental import Experimental

@Experimental
# This class is Experiemental and may change in future releases.
class MonetaryAmountInput: 
    """
    Represents a monetary amount with a currency code.
    """

    def __init__(
        self, 
        value: Decimal = None,
        currency_code: str = None
    ):

        self._value = value 
        self._currency_code = currency_code 


    def to_graphql_variables(self) -> Dict: 
        """
        Returns a dictionary representing the input object, to pass as variables to a GraphQL mutation.
        """
        variables = {}
        if self._value is not None: 
            variables["value"] = str(self._value)
        if self._currency_code is not None: 
            variables["currencyCode"] = self._currency_code
        
        return variables