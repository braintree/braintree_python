from tests.test_helper import *

class TestTransactionLineItem(unittest.TestCase):
    def test_find_all_traversal_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "transaction line items with id '\\.\\./\\.\\./foo' not found"):
            TransactionLineItem.find_all("../../foo")
