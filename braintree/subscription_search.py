from braintree.util import Constants
from braintree import Subscription
from braintree.search import Search

class SubscriptionSearch:
    billing_cycles_remaining = Search.RangeNodeBuilder("billing_cycles_remaining")
    days_past_due = Search.RangeNodeBuilder("days_past_due")
    id = Search.TextNodeBuilder("id")
    ids = Search.MultipleValueNodeBuilder("ids")
    in_trial_period = Search.MultipleValueNodeBuilder("in_trial_period")
    merchant_account_id = Search.MultipleValueNodeBuilder("merchant_account_id")
    plan_id = Search.MultipleValueOrTextNodeBuilder("plan_id")
    price = Search.RangeNodeBuilder("price")
    status = Search.MultipleValueNodeBuilder("status", Constants.get_all_constant_values_from_class(Subscription.Status))
