from tests.test_helper import *

class TestEuropeBankAccount(unittest.TestCase):
    def test_mandate_type_constants(self):
        self.assertEquals("business", EuropeBankAccount.MandateType.Business)
        self.assertEquals("consumer", EuropeBankAccount.MandateType.Consumer)
