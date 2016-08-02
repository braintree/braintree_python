from tests.test_helper import *

class TestConstants(unittest.TestCase):
    def test_get_all_constant_values_from_class(self):
        self.assertEqual(["Active", "Canceled", "Expired", "Past Due", "Pending"], Constants.get_all_constant_values_from_class(Subscription.Status))
