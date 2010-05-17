from braintree.search import Search

class SubscriptionSearch:
    plan_id = Search.TextNodeBuilder("plan_id")
    days_past_due = Search.TextNodeBuilder("days_past_due")
    status = Search.MultipleValueNodeBuilder("status")
    ids = Search.MultipleValueNodeBuilder("ids")
