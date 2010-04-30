from braintree.credit_card import CreditCard
from braintree.search import Search
from braintree.transaction import Transaction

class TransactionSearch:
    billing_first_name           = Search.TextNodeBuilder("billing_first_name")
    billing_company              = Search.TextNodeBuilder("billing_company")
    billing_country_name         = Search.TextNodeBuilder("billing_country_name")
    billing_extended_address     = Search.TextNodeBuilder("billing_extended_address")
    billing_first_name           = Search.TextNodeBuilder("billing_first_name")
    billing_last_name            = Search.TextNodeBuilder("billing_last_name")
    billing_locality             = Search.TextNodeBuilder("billing_locality")
    billing_postal_code          = Search.TextNodeBuilder("billing_postal_code")
    billing_region               = Search.TextNodeBuilder("billing_region")
    billing_street_address       = Search.TextNodeBuilder("billing_street_address")
    credit_card_cardholder_name  = Search.TextNodeBuilder("credit_card_cardholder_name")
    currency                     = Search.TextNodeBuilder("currency")
    customer_company             = Search.TextNodeBuilder("customer_company")
    customer_email               = Search.TextNodeBuilder("customer_email")
    customer_fax                 = Search.TextNodeBuilder("customer_fax")
    customer_first_name          = Search.TextNodeBuilder("customer_first_name")
    customer_id                  = Search.TextNodeBuilder("customer_id")
    customer_last_name           = Search.TextNodeBuilder("customer_last_name")
    customer_phone               = Search.TextNodeBuilder("customer_phone")
    customer_website             = Search.TextNodeBuilder("customer_website")
    id                           = Search.TextNodeBuilder("id")
    order_id                     = Search.TextNodeBuilder("order_id")
    payment_method_token         = Search.TextNodeBuilder("payment_method_token")
    processor_authorization_code = Search.TextNodeBuilder("processor_authorization_code")
    shipping_company             = Search.TextNodeBuilder("shipping_company")
    shipping_country_name        = Search.TextNodeBuilder("shipping_country_name")
    shipping_extended_address    = Search.TextNodeBuilder("shipping_extended_address")
    shipping_first_name          = Search.TextNodeBuilder("shipping_first_name")
    shipping_last_name           = Search.TextNodeBuilder("shipping_last_name")
    shipping_locality            = Search.TextNodeBuilder("shipping_locality")
    shipping_postal_code         = Search.TextNodeBuilder("shipping_postal_code")
    shipping_region              = Search.TextNodeBuilder("shipping_region")
    shipping_street_address      = Search.TextNodeBuilder("shipping_street_address")

    credit_card_expiration_date  = Search.EqualityNodeBuilder("credit_card_expiration_date")
    credit_card_number           = Search.PartialMatchNodeBuilder("credit_card_number")

    merchant_account_id          = Search.MultipleValueNodeBuilder("merchant_account_id")

    created_using = Search.MultipleValueNodeBuilder("created_using", [
        Transaction.CreatedUsing.FullInformation,
        Transaction.CreatedUsing.Token
    ])

    credit_card_card_type = Search.MultipleValueNodeBuilder("credit_card_card_type", [
        CreditCard.CardType.AmEx,
        CreditCard.CardType.CarteBlanche,
        CreditCard.CardType.ChinaUnionPay,
        CreditCard.CardType.DinersClubInternational,
        CreditCard.CardType.Discover,
        CreditCard.CardType.JCB,
        CreditCard.CardType.Laser,
        CreditCard.CardType.Maestro,
        CreditCard.CardType.MasterCard,
        CreditCard.CardType.Solo,
        CreditCard.CardType.Switch,
        CreditCard.CardType.Visa,
        CreditCard.CardType.Unknown
    ])

    credit_card_customer_location = Search.MultipleValueNodeBuilder("credit_card_customer_location", [
        CreditCard.CustomerLocation.International,
        CreditCard.CustomerLocation.US
    ])

    source = Search.MultipleValueNodeBuilder("source", [
        Transaction.Source.Api,
        Transaction.Source.ControlPanel,
        Transaction.Source.Recurring
    ])

    status = Search.MultipleValueNodeBuilder("status", [
        Transaction.Status.Authorized,
        Transaction.Status.Authorizing,
        Transaction.Status.Failed,
        Transaction.Status.GatewayRejected,
        Transaction.Status.ProcessorDeclined,
        Transaction.Status.Settled,
        Transaction.Status.SettlementFailed,
        Transaction.Status.SubmittedForSettlement,
        Transaction.Status.Unknown,
        Transaction.Status.Unrecognized,
        Transaction.Status.Voided
    ])

    type = Search.MultipleValueNodeBuilder("type", [
        Transaction.Type.Credit,
        Transaction.Type.Sale
    ])

    refund = Search.KeyValueNodeBuilder("refund")

    amount = Search.RangeNodeBuilder("amount")
    created_at = Search.RangeNodeBuilder("created_at")
