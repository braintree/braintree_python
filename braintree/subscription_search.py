from braintree.search import Search

class SubscriptionSearch:
    plan_id = Search.TextNode("plan_id")
    days_past_due = Search.TextNode("days_past_due")
    status = Search.MultipleValueNode("status")
