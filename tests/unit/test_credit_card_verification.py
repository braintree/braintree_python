from tests.test_helper import *

class TestCreditCardVerification(unittest.TestCase):

    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_create_raises_exception_with_bad_keys(self):
        CreditCardVerification.create({"bad_key": "value", "credit_card": {"number": "value"}})

    def test_constructor_with_amount(self):
        attributes = {
            'amount': '27.00',
            'currency_iso_code': 'USD'
        }
        verification = CreditCardVerification(None, attributes)

        self.assertEqual(verification.amount, Decimal('27.00'))
        self.assertEqual(verification.currency_iso_code, 'USD')

    def test_constructor_when_risk_data_is_not_included(self):
        verification = CreditCardVerification(None, {"amount": "1.00"})
        self.assertEqual(verification.risk_data, None)

    @raises(NotFoundError)
    def test_finding_empty_id_raises_not_found_exception(self):
        CreditCardVerification.find(" ")

    @raises(NotFoundError)
    def test_finding_none_raises_not_found_exception(self):
        CreditCardVerification.find(None)
