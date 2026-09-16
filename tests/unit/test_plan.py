from tests.test_helper import *

class TestPlan(unittest.TestCase):
    def test_find_traversal_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "Plan with id '\\.\\./\\.\\./foo' not found"):
            Plan.find("../../foo")

    def test_update_traversal_id_raises_not_found_exception(self):
        with self.assertRaisesRegex(NotFoundError, "Plan with id '\\.\\./\\.\\./foo' not found"):
            Plan.update("../../foo", {})
