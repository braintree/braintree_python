from tests.test_helper import *

class TestTransactionLineItemGateway(unittest.TestCase):

    def test_transaction_line_item_gateway_find_all_raises_when_transaction_not_found(self):
        with self.assertRaises(NotFoundError):
            transaction_id = "willnotbefound"
            TransactionLineItem.find_all(transaction_id)
