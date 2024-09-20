from tests.test_helper import *

class TestCreditCardVerification(unittest.TestCase):

    def test_create_raises_exception_with_bad_keys(self):
        with self.assertRaisesRegex(KeyError, "'Invalid keys: bad_key'"):
            CreditCardVerification.create({"bad_key": "value", "credit_card": {"number": "value"}})

    def test_create_signature(self):
        billing_address_params = [
                "company", "country_code_alpha2", "country_code_alpha3", "country_code_numeric",
                "country_name", "extended_address", "first_name", "last_name", "locality",
                "postal_code", "region", "street_address"
                ]
        credit_card_params = [
                "number", "cvv", "cardholder_name", "cvv", "expiration_date", "expiration_month",
                "expiration_year", {"billing_address": billing_address_params}
                ]
        external_vault_params = [
                "previous_network_transaction_id",
                "status"
                ]
        options_params = [
                "account_type", "amount", "merchant_account_id"
                ]
        risk_data_params = [
                "customer_browser",
                "customer_ip"
                ]
        three_d_secure_pass_thru_params = [
                "eci_flag",
                "cavv",
                "xid",
                "authentication_response",
                "directory_response",
                "cavv_algorithm",
                "ds_transaction_id",
                "three_d_secure_version"
                ]
        expected = [
                {"credit_card": credit_card_params},
                {"external_vault": external_vault_params},
                "intended_transaction_source",
                {"options": options_params},
                "payment_method_nonce",
                {"risk_data": risk_data_params},
                "three_d_secure_authentication_id",
                {"three_d_secure_pass_thru": three_d_secure_pass_thru_params}]

        self.assertEqual(expected, CreditCardVerification.create_signature())

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

    def test_constructor_when_ani_result_code_is_included(self):
        attributes = {
            'ani_first_name_response_code': 'M',
            'ani_last_name_response_code': 'N'
        }
        verification = CreditCardVerification(None, attributes)
        self.assertEqual(verification.ani_first_name_response_code, 'M')
        self.assertEqual(verification.ani_last_name_response_code, 'N')

    def test_finding_empty_id_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            CreditCardVerification.find(" ")

    def test_finding_none_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            CreditCardVerification.find(None)
