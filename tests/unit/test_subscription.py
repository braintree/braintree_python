from tests.test_helper import *

class TestSubscription(unittest.TestCase):
    def test_create_raises_exception_with_bad_keys(self):
        try:
            Subscription.create({"bad_key": "value"})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_update_raises_exception_with_bad_keys(self):
        try:
            Subscription.update("id", {"bad_key": "value"})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_finding_empty_id_raises_not_found_exception(self):
        try:
            Subscription.find(" ")
            self.assertTrue(False)
        except NotFoundError as e:
            self.assertTrue(True)
