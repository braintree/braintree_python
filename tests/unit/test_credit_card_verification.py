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

    def test_constructor_with_bad_amount(self):
        attributes = {
            'amount': None
        }
        verification = CreditCardVerification(None, attributes)

        self.assertEqual(verification.amount, None)

    def test_constructor_without_amount(self):
        verification = CreditCardVerification(None, {})

        self.assertEqual(verification.amount, None)
        self.assertEqual(verification.currency_iso_code, None)

    def test_constructor_when_risk_data_is_not_included(self):
        verification = CreditCardVerification(None, {"amount": "1.00"})
        self.assertEqual(verification.risk_data, None)

    def test_constructor_when_network_response_is_included(self):
        attributes = {
            'amount': '1.00',
            'network_response_code': '00',
            'network_response_text': 'Successful approval/completion or V.I.P. PIN verification is successful'
        }
        verification = CreditCardVerification(None, attributes)
        self.assertEqual(verification.network_response_code, '00')
        self.assertEqual(verification.network_response_text, 'Successful approval/completion or V.I.P. PIN verification is successful')

    def test_constructor_when_network_response_is_not_included(self):
        verification = CreditCardVerification(None, {'amount': '1.00'})
        self.assertEqual(verification.network_response_code, None)
        self.assertEqual(verification.network_response_text, None)

    @raises(NotFoundError)
    def test_finding_empty_id_raises_not_found_exception(self):
        CreditCardVerification.find(" ")

    @raises(NotFoundError)
    def test_finding_none_raises_not_found_exception(self):
        CreditCardVerification.find(None)
