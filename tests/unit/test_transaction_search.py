from tests.test_helper import *

class TestTransactionSearch(unittest.TestCase):
    def _serialize(self, node):
        return {node.name: node.to_param()}

    def test_ach_type_in_list_same_day(self):
        node = TransactionSearch.ach_type.in_list([Transaction.AchType.SameDay])
        self.assertEqual({"ach_type": ["same_day"]}, self._serialize(node))

    def test_ach_type_in_list_standard(self):
        node = TransactionSearch.ach_type.in_list([Transaction.AchType.Standard])
        self.assertEqual({"ach_type": ["standard"]}, self._serialize(node))

    def test_ach_type_in_list_both(self):
        node = TransactionSearch.ach_type.in_list([Transaction.AchType.SameDay, Transaction.AchType.Standard])
        self.assertEqual({"ach_type": ["same_day", "standard"]}, self._serialize(node))

    def test_ach_type_is_same_day(self):
        node = TransactionSearch.ach_type == Transaction.AchType.SameDay
        self.assertEqual({"ach_type": ["same_day"]}, self._serialize(node))

    def test_ach_type_is_standard(self):
        node = TransactionSearch.ach_type == Transaction.AchType.Standard
        self.assertEqual({"ach_type": ["standard"]}, self._serialize(node))

    def test_ach_type_with_value_not_in_whitelist(self):
        with self.assertRaisesRegex(AttributeError, r"Invalid argument\(s\) for ach_type: noSuchAchType"):
            TransactionSearch.ach_type == "noSuchAchType"
