import unittest
import tests.test_helper
from braintree.environment import Environment
from braintree.configuration import Configuration

class TestConfiguration(unittest.TestCase):
    def test_base_merchant_path_for_development(self):
        self.assertTrue("/merchants/integration_merchnat_id", Configuration.base_merchant_path())
