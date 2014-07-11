from tests.test_helper import *

class TestSEPABankAccount(unittest.TestCase):
    def test_mandate_type_constants(self):
        self.assertEquals("business", SEPABankAccount.MandateType.Business)
        self.assertEquals("consumer", SEPABankAccount.MandateType.Consumer)
