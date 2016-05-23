from tests.test_helper import *

class TestCreditCardVerification(unittest.TestCase):

    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_create_raises_exception_with_bad_keys(self):
        CreditCardVerification.create({"bad_key": "value", "credit_card": {"number": "value"}})

    def test_when_risk_data_is_not_included(self):
        verification = CreditCardVerification(None, {})
        self.assertEquals(verification.risk_data, None)

    @raises(NotFoundError)
    def test_finding_empty_id_raises_not_found_exception(self):
        CreditCardVerification.find(" ")

    @raises(NotFoundError)
    def test_finding_none_raises_not_found_exception(self):
        CreditCardVerification.find(None)
