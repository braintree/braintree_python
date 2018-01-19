import braintree
import warnings

from braintree.attribute_getter import AttributeGetter
from braintree.resource import Resource

class TransactionLineItem(AttributeGetter):
    pass

    class Kind(object):
        """
        Constants representing transaction line item kinds. Available kinds are:

        * braintree.TransactionLineItem.Kind.Credit
        * braintree.TransactionLineItem.Kind.Debit
        """

        Credit = "credit"
        Debit = "debit"

    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)
