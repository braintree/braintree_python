from tests.test_helper import *
from braintree.test.nonces import Nonces
from datetime import date

class TestPaymentMethodNonce(unittest.TestCase):
    indian_payment_token = "india_visa_credit"
    european_payment_token = "european_visa_credit"
    indian_merchant_token = "india_three_d_secure_merchant_account"
    european_merchant_token = "european_three_d_secure_merchant_account"
    amount_threshold_for_rbi = 2000

    def test_create_nonce_from_payment_method(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "customer_id": customer_id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
        })

        result = PaymentMethodNonce.create(credit_card_result.credit_card.token)

        self.assertTrue(result.is_success)
        self.assertNotEqual(None, result.payment_method_nonce)
        self.assertNotEqual(None, result.payment_method_nonce.nonce)

    def test_create_nonce_from_payment_method_with_invalid_params(self):
        nonce_request = {
            "merchant_account_id": self.indian_merchant_token,
            "authentication_insight": True,
            "invalid_keys": "foo"
        }
        params = {"payment_method_nonce": nonce_request}

        with self.assertRaises(KeyError):
            PaymentMethodNonce.create(self.indian_payment_token, params)

    def test_create_nonce_with_auth_insight_regulation_environment_unavailable(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "customer_id": customer_id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
        })
        auth_insight_result = self._request_authentication_insights(self.indian_merchant_token, credit_card_result.credit_card.token)
        self.assertEqual("unavailable", auth_insight_result["regulation_environment"])

    def test_create_nonce_with_auth_insight_regulation_environment_unregulated(self):
        auth_insight_result = self._request_authentication_insights(self.european_merchant_token, self.indian_payment_token)
        self.assertEqual("unregulated", auth_insight_result["regulation_environment"])

    def test_create_nonce_with_auth_insight_regulation_environment_psd2(self):
        auth_insight_result = self._request_authentication_insights(self.european_merchant_token, self.european_payment_token)
        self.assertEqual("psd2", auth_insight_result["regulation_environment"])

    def test_create_nonce_with_auth_insight_regulation_environment_rbi(self):
        auth_insight_result = self._request_authentication_insights(self.indian_merchant_token, self.indian_payment_token, self.amount_threshold_for_rbi)
        self.assertEqual("rbi", auth_insight_result["regulation_environment"])

    def test_create_nonce_with_auth_insight_sca_indicator_unavailable(self):
        auth_insight_result = self._request_authentication_insights(self.indian_merchant_token, self.indian_payment_token)
        self.assertEqual("unavailable", auth_insight_result["sca_indicator"])

    def test_create_nonce_with_auth_insight_sca_indicator_sca_required(self):
        auth_insight_result = self._request_authentication_insights(self.indian_merchant_token, self.indian_payment_token, self.amount_threshold_for_rbi + 1)
        self.assertEqual("sca_required", auth_insight_result["sca_indicator"])

    def test_create_nonce_with_auth_insight_sca_indicator_sca_optional(self):
        auth_insight_result = self._request_authentication_insights(self.indian_merchant_token, self.indian_payment_token, self.amount_threshold_for_rbi, False, None)
        self.assertEqual("sca_optional", auth_insight_result["sca_indicator"])

    def test_create_nonce_with_auth_insight_sca_indicator_sca_required_with_recurring_customer_consent_and_max_amount(self):
        auth_insight_result = self._request_authentication_insights(self.indian_merchant_token, self.indian_payment_token, self.amount_threshold_for_rbi, True, 1000)
        self.assertEqual("sca_required", auth_insight_result["sca_indicator"])

    def test_create_raises_not_found_when_404(self):
        self.assertRaises(NotFoundError, PaymentMethodNonce.create, "not-a-token")

    def test_find_nonce_shows_details(self):
        config = Configuration(
            environment=Environment.Development,
            merchant_id="integration_merchant_id",
            public_key="integration_public_key",
            private_key="integration_private_key"
        )
        gateway = BraintreeGateway(config)

        nonce = PaymentMethodNonce.find("fake-valid-visa-nonce")

        self.assertEqual("401288", nonce.details["bin"])

    def test_find_nonce_shows_3ds_details(self):
        config = Configuration(
            environment=Environment.Development,
            merchant_id="integration_merchant_id",
            public_key="integration_public_key",
            private_key="integration_private_key"
        )
        gateway = BraintreeGateway(config)

        nonce = "fake-three-d-secure-visa-full-authentication-nonce"
        found_nonce = PaymentMethodNonce.find(nonce)
        three_d_secure_info = found_nonce.three_d_secure_info

        self.assertEqual("CreditCard", found_nonce.type)
        self.assertEqual(nonce, found_nonce.nonce)
        self.assertEqual("authenticate_successful", three_d_secure_info.status)
        self.assertEqual(True, three_d_secure_info.liability_shifted)
        self.assertEqual(True, three_d_secure_info.liability_shift_possible)
        self.assertIsInstance(three_d_secure_info.enrolled, str)
        self.assertIsInstance(three_d_secure_info.cavv, str)
        self.assertIsInstance(three_d_secure_info.xid, str)
        self.assertIsInstance(three_d_secure_info.eci_flag, str)
        self.assertIsInstance(three_d_secure_info.three_d_secure_version, str)
        self.assertIsInstance(three_d_secure_info.three_d_secure_authentication_id, str)

    def test_find_nonce_shows_paypal_details(self):
        found_nonce = PaymentMethodNonce.find("fake-google-pay-paypal-nonce")

        self.assertNotEqual(None, found_nonce.details["payer_info"]["first_name"])
        self.assertNotEqual(None, found_nonce.details["payer_info"]["last_name"])
        self.assertNotEqual(None, found_nonce.details["payer_info"]["email"])
        self.assertNotEqual(None, found_nonce.details["payer_info"]["payer_id"])

    def test_find_nonce_shows_venmo_details(self):
        found_nonce = PaymentMethodNonce.find("fake-venmo-account-nonce")

        self.assertEqual("99", found_nonce.details["last_two"])
        self.assertEqual("venmojoe", found_nonce.details["username"])
        self.assertEqual("1234567891234567891", found_nonce.details["venmo_user_id"])

    def test_find_nonce_shows_sepa_direct_debit_details(self):
        found_nonce = PaymentMethodNonce.find(Nonces.SepaDirectDebit)

        self.assertEqual("1234", found_nonce.details["last_4"])
        self.assertEqual("RECURRENT", found_nonce.details["mandate_type"])
        self.assertEqual("a-fake-bank-reference-token", found_nonce.details["bank_reference_token"])
        self.assertEqual("a-fake-mp-customer-id", found_nonce.details["merchant_or_partner_customer_id"])

    def test_find_nonce_shows_meta_checkout_card_details(self):
        found_nonce = PaymentMethodNonce.find(Nonces.MetaCheckoutCard)

        self.assertEqual("401288", found_nonce.details["bin"])
        self.assertEqual("81", found_nonce.details["last_two"])
        self.assertEqual("1881", found_nonce.details["last_four"])
        self.assertEqual("Visa", found_nonce.details["card_type"])
        self.assertEqual("Meta Checkout Card Cardholder", found_nonce.details["cardholder_name"])
        self.assertEqual(str(date.today().year + 1), found_nonce.details["expiration_year"])
        self.assertEqual("12", found_nonce.details["expiration_month"])

    def test_find_nonce_shows_meta_checkout_token_details(self):
        found_nonce = PaymentMethodNonce.find(Nonces.MetaCheckoutToken)

        self.assertEqual("401288", found_nonce.details["bin"])
        self.assertEqual("81", found_nonce.details["last_two"])
        self.assertEqual("1881", found_nonce.details["last_four"])
        self.assertEqual("Visa", found_nonce.details["card_type"])
        self.assertEqual("Meta Checkout Token Cardholder", found_nonce.details["cardholder_name"])
        self.assertEqual(str(date.today().year + 1), found_nonce.details["expiration_year"])
        self.assertEqual("12", found_nonce.details["expiration_month"])

    def test_exposes_null_3ds_info_if_none_exists(self):
        http = ClientApiHttp.create()

        _, nonce = http.get_paypal_nonce({
            "consent-code": "consent-code",
            "access-token": "access-token",
            "options": {"validate": False}
        })

        found_nonce = PaymentMethodNonce.find(nonce)

        self.assertEqual(nonce, found_nonce.nonce)
        self.assertEqual(None, found_nonce.three_d_secure_info)

    def test_find_raises_not_found_when_404(self):
        self.assertRaises(NotFoundError, PaymentMethodNonce.find, "not-a-nonce")

    def test_bin_data_has_commercial(self):
        found_nonce = PaymentMethodNonce.find("fake-valid-commercial-nonce")
        bin_data = found_nonce.bin_data

        self.assertEqual(CreditCard.Commercial.Yes, bin_data.commercial)

    def test_bin_data_has_country_of_issuance(self):
        found_nonce = PaymentMethodNonce.find("fake-valid-country-of-issuance-cad-nonce")
        bin_data = found_nonce.bin_data

        self.assertEqual("CAN", bin_data.country_of_issuance)

    def test_bin_data_debit(self):
        found_nonce = PaymentMethodNonce.find("fake-valid-debit-nonce")
        bin_data = found_nonce.bin_data

        self.assertEqual(CreditCard.Debit.Yes, bin_data.debit)

    def test_bin_data_durbin_regulated(self):
        found_nonce = PaymentMethodNonce.find("fake-valid-durbin-regulated-nonce")
        bin_data = found_nonce.bin_data

        self.assertEqual(CreditCard.DurbinRegulated.Yes, bin_data.durbin_regulated)

    def test_bin_data_issuing_bank(self):
        found_nonce = PaymentMethodNonce.find("fake-valid-issuing-bank-network-only-nonce")
        bin_data = found_nonce.bin_data

        self.assertEqual("NETWORK ONLY", bin_data.issuing_bank)

    def test_bin_data_payroll(self):
        found_nonce = PaymentMethodNonce.find("fake-valid-payroll-nonce")
        bin_data = found_nonce.bin_data

        self.assertEqual(CreditCard.Payroll.Yes, bin_data.payroll)

    def test_bin_data_prepaid(self):
        found_nonce = PaymentMethodNonce.find("fake-valid-prepaid-nonce")
        bin_data = found_nonce.bin_data

        self.assertEqual(CreditCard.Prepaid.Yes, bin_data.prepaid)

    def test_bin_data_prepaid_reloadable(self):
        found_nonce = PaymentMethodNonce.find("fake-valid-prepaid-reloadable-nonce")
        bin_data = found_nonce.bin_data

        self.assertEqual(CreditCard.PrepaidReloadable.Yes, bin_data.prepaid_reloadable)

    def test_bin_data_unknown_values(self):
        found_nonce = PaymentMethodNonce.find("fake-valid-unknown-indicators-nonce")
        bin_data = found_nonce.bin_data

        self.assertEqual(CreditCard.Commercial.Unknown, bin_data.commercial)
        self.assertEqual(CreditCard.CountryOfIssuance.Unknown, bin_data.country_of_issuance)
        self.assertEqual(CreditCard.Debit.Unknown, bin_data.debit)
        self.assertEqual(CreditCard.DurbinRegulated.Unknown, bin_data.durbin_regulated)
        self.assertEqual(CreditCard.Healthcare.Unknown, bin_data.healthcare)
        self.assertEqual(CreditCard.IssuingBank.Unknown, bin_data.issuing_bank)
        self.assertEqual(CreditCard.Payroll.Unknown, bin_data.payroll)
        self.assertEqual(CreditCard.Prepaid.Unknown, bin_data.prepaid)
        self.assertEqual(CreditCard.PrepaidReloadable.Unknown, bin_data.prepaid_reloadable)
        self.assertEqual(CreditCard.ProductId.Unknown, bin_data.product_id)

    def _request_authentication_insights(self, merchant_account_id, payment_method_token, amount = None, recurring_customer_consent = None, recurring_max_amount = None):
        nonce_request = {
            "merchant_account_id": merchant_account_id,
            "authentication_insight": True,
            "authentication_insight_options": {
                "amount": amount,
                "recurring_customer_consent": recurring_customer_consent,
                "recurring_max_amount": recurring_max_amount,
             }
        }
        result = PaymentMethodNonce.create(payment_method_token, {"payment_method_nonce": nonce_request})
        return result.payment_method_nonce.authentication_insight
