from decimal import Decimal
from braintree.attribute_getter import AttributeGetter
from braintree.transaction_details import TransactionDetails
from braintree.dispute_details import DisputeEvidence, DisputeStatusHistory
from braintree.configuration import Configuration

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
        * braintree.Dispute.Reason.Retrieval
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
        Retrieval                     = "retrieval"
        TransactionAmountDiffers      = "transaction_amount_differs"

    class Kind(object):
        """
        Constants representing dispute kinds. Available types are:

        * braintree.Dispute.Kind.Chargeback
        * braintree.Dispute.Kind.PreArbitration
        * braintree.Dispute.Kind.Retrieval
        """
        Chargeback     = "chargeback"
        PreArbitration = "pre_arbitration"
        Retrieval      = "retrieval"

    @staticmethod
    def find(id):
        return Configuration.gateway().dispute.find(id)

    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)

        if "amount" in attributes and self.amount is not None:
            self.amount = Decimal(self.amount)
        if "amount_disputed" in attributes and self.amount_disputed is not None:
            self.amount_disputed = Decimal(self.amount_disputed)
        if "amount_won" in attributes and self.amount_won is not None:
            self.amount_won = Decimal(self.amount_won)
        if "transaction" in attributes:
            self.transaction_details = TransactionDetails(attributes.pop("transaction"))
            self.transaction = self.transaction_details
        if "evidence" in attributes and self.evidence is not None:
            self.evidence = [DisputeEvidence(evidence) for evidence in self.evidence]
        if "status_history" in attributes and self.status_history is not None:
            self.status_history = [DisputeStatusHistory(status_history) for status_history in self.status_history]
