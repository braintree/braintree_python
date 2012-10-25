from braintree.credit_card import CreditCard
from braintree.search import Search
from braintree.util import Constants

class CreditCardVerificationSearch:
    credit_card_cardholder_name  = Search.TextNodeBuilder("credit_card_cardholder_name")
    id                           = Search.TextNodeBuilder("id")
    credit_card_expiration_date  = Search.EqualityNodeBuilder("credit_card_expiration_date")
    credit_card_number           = Search.PartialMatchNodeBuilder("credit_card_number")
    status                       = Search.MultipleValueNodeBuilder("credit_card_type", Constants.get_all_constant_values_from_class(CreditCard.CardType))
    ids                          = Search.MultipleValueNodeBuilder("ids")
    created_at                   = Search.RangeNodeBuilder("created_at")
