from tests.test_helper import *

class TestPayPalAccount(unittest.TestCase):
    def test_find_traversal_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "paypal account with token '\\.\\./\\.\\./foo' not found"):
            PayPalAccount.find("../../foo")

    def test_delete_traversal_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "paypal account with token '\\.\\./\\.\\./foo' not found"):
            PayPalAccount.delete("../../foo")

    def test_update_traversal_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "paypal account with token '\\.\\./\\.\\./foo' not found"):
            PayPalAccount.update("../../foo", {})
