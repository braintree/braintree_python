from tests.test_helper import *

class TestEuropeBankAccount(unittest.TestCase):
    def test_mandate_type_constants(self):
        self.assertEqual("business", EuropeBankAccount.MandateType.Business)
        self.assertEqual("consumer", EuropeBankAccount.MandateType.Consumer)
