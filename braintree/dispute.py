from decimal import Decimal
from braintree.attribute_getter import AttributeGetter
from braintree.transaction_details import TransactionDetails

class Dispute(AttributeGetter):
    class Status(object):
        """
        Constants representing dispute statuses. Available types are:

        * braintree.Dispute.Status.Open
        * braintree.Dispute.Status.Won
        * braintree.Dispute.Status.Lost
        """
        Open  = "open"
        Won  = "won"
        Lost = "lost"

    class Reason(object):
        """
        Constants representing dispute reasons. Available types are:

        * braintree.Dispute.Reason.CancelledRecurringTransaction
        * braintree.Dispute.Reason.CreditNotProcessed
        * braintree.Dispute.Reason.Duplicate
        * braintree.Dispute.Reason.Fraud
        * braintree.Dispute.Reason.General
        * braintree.Dispute.Reason.InvalidAccount
        * braintree.Dispute.Reason.NotRecognized
        * braintree.Dispute.Reason.ProductNotReceived
        * braintree.Dispute.Reason.ProductUnsatisfactory
        * braintree.Dispute.Reason.TransactionAmountDiffers
        """
        CancelledRecurringTransaction = "cancelled_recurring_transaction"
        CreditNotProcessed            = "credit_not_processed"
        Duplicate                     = "duplicate"
        Fraud                         = "fraud"
        General                       = "general"
        InvalidAccount                = "invalid_account"
        NotRecognized                 = "not_recognized"
        ProductNotReceived            = "product_not_received"
        ProductUnsatisfactory         = "product_unsatisfactory"
        TransactionAmountDiffers      = "transaction_amount_differs"


    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)

        if self.amount is not None:
            self.amount = Decimal(self.amount)
        if "transaction" in attributes:
            self.transaction_details = TransactionDetails(attributes.pop("transaction"))
