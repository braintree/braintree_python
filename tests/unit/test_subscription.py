from tests.test_helper import *

class TestSubscription(unittest.TestCase):
    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_create_raises_exception_with_bad_keys(self):
        Subscription.create({"bad_key": "value"})

    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_update_raises_exception_with_bad_keys(self):
        Subscription.update("id", {"bad_key": "value"})

    @raises(NotFoundError)
    def test_finding_empty_id_raises_not_found_exception(self):
        Subscription.find(" ")
