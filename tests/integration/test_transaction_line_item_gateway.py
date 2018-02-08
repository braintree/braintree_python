from tests.test_helper import *

class TestTransactionLineItemGateway(unittest.TestCase):

    @raises(NotFoundError)
    def test_transaction_line_item_gateway_find_all_raises_when_transaction_not_found(self):
        transaction_id = "willnotbefound"
        TransactionLineItem.find_all(transaction_id)
