from braintree.search import Search

class DisputeSearch:
    amount_disputed             =   Search.RangeNodeBuilder("amount_disputed")
    amount_won                  =   Search.RangeNodeBuilder("amount_won")
    case_number                 =   Search.TextNodeBuilder("case_number")
    # NEXT_MAJOR_VERSION Remove this attribute
    # DEPRECATED The chargeback_protection_level attribute is deprecated in favor of protection_level
    chargeback_protection_level =   Search.MultipleValueNodeBuilder("chargeback_protection_level")
    protection_level            =   Search.MultipleValueNodeBuilder("protection_level")
    customer_id                 =   Search.TextNodeBuilder("customer_id")
    disbursement_date           =   Search.RangeNodeBuilder("disbursement_date")
    effective_date              =   Search.RangeNodeBuilder("effective_date")
    id                          =   Search.TextNodeBuilder("id")
    kind                        =   Search.MultipleValueNodeBuilder("kind")
    merchant_account_id         =   Search.MultipleValueNodeBuilder("merchant_account_id")
    pre_dispute_program         =   Search.MultipleValueNodeBuilder("pre_dispute_program")
    reason                      =   Search.MultipleValueNodeBuilder("reason")
    reason_code                 =   Search.MultipleValueNodeBuilder("reason_code")
    received_date               =   Search.RangeNodeBuilder("received_date")
    reference_number            =   Search.TextNodeBuilder("reference_number")
    reply_by_date               =   Search.RangeNodeBuilder("reply_by_date")
    status                      =   Search.MultipleValueNodeBuilder("status")
    transaction_id              =   Search.TextNodeBuilder("transaction_id")
    transaction_source          =   Search.MultipleValueNodeBuilder("transaction_source")
