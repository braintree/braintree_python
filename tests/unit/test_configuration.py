from tests.test_helper import *

class TestConfiguration(unittest.TestCase):
    def test_base_merchant_path_for_development(self):
        self.assertTrue("/merchants/integration_merchnat_id", Configuration.instantiate().base_merchant_path())

    def test_default_ssl_package(self):
        self.assertTrue("m2crypto", Configuration.instantiate().ssl_package)

