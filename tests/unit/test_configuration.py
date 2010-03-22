from tests.test_helper import *

class TestConfiguration(unittest.TestCase):
    def test_base_merchant_path_for_development(self):
        self.assertTrue("/merchants/integration_merchnat_id", Configuration.base_merchant_path())
