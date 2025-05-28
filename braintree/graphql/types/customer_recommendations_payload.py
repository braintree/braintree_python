from typing import Dict, List, Any, Optional
from braintree.exceptions.server_error import ServerError
from braintree.graphql.enums.recommended_payment_option import RecommendedPaymentOption
from braintree.graphql.unions.customer_recommendations import CustomerRecommendations
from braintree.graphql.types.payment_options import PaymentOptions
from braintree.graphql.types.payment_recommendation import PaymentRecommendation
from braintree.util.experimental import Experimental

@Experimental
# This class is Experiemental and may change in future releases.
class CustomerRecommendationsPayload:
    """
    Represents the customer recommendations information associated with a PayPal customer session.
    """

    def __init__(self, is_in_paypal_network: bool = None, recommendations: CustomerRecommendations = None, response: Dict[str, Any] = None):
        if response:
            # Constructor for response map
            self.is_in_paypal_network = self._get_value(response, "generateCustomerRecommendations.isInPayPalNetwork")
            self.recommendations = self._extract_recommendations(response)
        else:
            # Constructor for direct values
            self.is_in_paypal_network = is_in_paypal_network
            self.recommendations = recommendations

    def _extract_recommendations(self, response: Dict[str, Any]) -> CustomerRecommendations:
        """
        Extract recommendations from the GraphQL response.
        
        Args:
            response: The GraphQL response containing recommendations data
            
        Returns:
            CustomerRecommendations object with payment options
        
        Raises:
            ServerError: If there's an error parsing the response
        """
        try:            
            payment_recommendations = self._get_value(response, "generateCustomerRecommendations.paymentRecommendations")
            
            payment_options_list = []
            payment_recommendations_list = []
            for i, recommendation in enumerate(payment_recommendations):
                
                recommended_priority = self._get_value(recommendation, "recommendedPriority")
                
                payment_option_string = self._get_value(recommendation, "paymentOption")
                
                payment_option = RecommendedPaymentOption(payment_option_string)
                
                payment_option_obj = PaymentOptions(payment_option, recommended_priority)
                payment_recommendation_obj = PaymentRecommendation(payment_option, recommended_priority)
                
                payment_options_list.append(payment_option_obj)
                payment_recommendations_list.append(payment_recommendation_obj)
            
            customer_recommendations = CustomerRecommendations(payment_recommendations = payment_recommendations_list)
            
            return customer_recommendations
        except Exception as e:
            import traceback
            raise ServerError(f"Error extracting recommendations: {str(e)}")

    @staticmethod
    def _get_value(response: Dict[str, Any], key: str) -> Any:
        """
        Get a nested value from a dictionary using dot notation.
        
        Args:
            response: The dictionary to extract values from
            key: Dot notation path to the desired value
            
        Returns:
            The value at the specified path
            
        Raises:
            ServerError: If the key doesn't exist in the dictionary
        """
        current_map = response
        key_parts = key.split('.')
        
        # Navigate through nested dictionaries for all but last key
        for i in range(len(key_parts) - 1):
            sub_key = key_parts[i]
            current_map = CustomerRecommendationsPayload._pop_value(current_map, sub_key)
        
        # Get the final value
        last_key = key_parts[-1]
        return CustomerRecommendationsPayload._pop_value(current_map, last_key)

    @staticmethod
    def _pop_value(response: Dict[str, Any], key: str) -> Any:
        """
        Get a value from a dictionary with error handling.
        
        Args:
            response: The dictionary to extract a value from
            key: The key to look up
            
        Returns:
            The value associated with the key
            
        Raises:
            ServerError: If the key doesn't exist in the dictionary
        """
        if key not in response:
            raise ServerError("Couldn't parse response")
        return response[key]
