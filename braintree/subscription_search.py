from braintree.util import Constants
from braintree import Subscription
from braintree.search import Search

class SubscriptionSearch:
    days_past_due = Search.RangeNodeBuilder("days_past_due")
    id = Search.TextNodeBuilder("id")
    ids = Search.MultipleValueNodeBuilder("ids")
    merchant_account_id = Search.MultipleValueNodeBuilder("merchant_account_id")
    plan_id = Search.TextNodeBuilder("plan_id")
    price = Search.RangeNodeBuilder("price")
    status = Search.MultipleValueNodeBuilder("status", Constants.get_all_constant_values_from_class(Subscription.Status))
