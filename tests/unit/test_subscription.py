from tests.test_helper import *

class TestSubscription(unittest.TestCase):
    def test_create_raises_exception_with_bad_keys(self):
        with self.assertRaisesRegex(KeyError, "'Invalid keys: bad_key'"):
            Subscription.create({"bad_key": "value"})

    def test_update_raises_exception_with_bad_keys(self):
        with self.assertRaisesRegex(KeyError, "'Invalid keys: bad_key'"):
            Subscription.update("id", {"bad_key": "value"})

    def test_finding_empty_id_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            Subscription.find(" ")

    def test_finding_None_id_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            Subscription.find(None)
