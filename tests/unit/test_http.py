from tests.test_helper import *

class TestHttp(unittest.TestCase):
    def test_raise_exception_from_status_for_upgrade_required(self):
        try:
            Http.raise_exception_from_status(426)
            self.assertTrue(False)
        except UpgradeRequiredError:
            pass
