import time
from datetime import datetime
from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers
from braintree.test.nonces import Nonces

class TestPaymentMethod(unittest.TestCase):
    def test_create_with_three_d_secure_nonce(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.ThreeDSecureVisaFullAuthentication,
            "options": {
                "verify_card": "true",
            }
        })

        self.assertTrue(result.is_success)

        three_d_secure_info = result.payment_method.verification.three_d_secure_info

        self.assertEqual("authenticate_successful", three_d_secure_info.status)
        self.assertEqual(True, three_d_secure_info.liability_shifted)
        self.assertEqual(True, three_d_secure_info.liability_shift_possible)
        self.assertIsInstance(three_d_secure_info.enrolled, str)
        self.assertIsInstance(three_d_secure_info.cavv, str)
        self.assertIsInstance(three_d_secure_info.xid, str)
        self.assertIsInstance(three_d_secure_info.eci_flag, str)
        self.assertIsInstance(three_d_secure_info.three_d_secure_version, str)

    def test_create_with_three_d_secure_pass_thru(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.Transactable,
            "three_d_secure_pass_thru": {
                "three_d_secure_version": "1.1.0",
                "eci_flag": "05",
                "cavv": "some-cavv",
                "xid": "some-xid"
            },
            "options": {
                "verify_card": "true",
            }
        })

        self.assertTrue(result.is_success)

    def test_create_with_three_d_secure_pass_thru_without_eci_flag(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.Transactable,
            "three_d_secure_pass_thru": {
                "three_d_secure_version": "1.1.0",
                "cavv": "some-cavv",
                "xid": "some-xid"
            },
            "options": {
                "verify_card": "true",
            }
        })

        self.assertFalse(result.is_success)
        self.assertEqual("EciFlag is required.", result.message)

    def test_create_with_paypal_billing_agreements_nonce(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.PayPalBillingAgreement
        })

        self.assertTrue(result.is_success)
        created_account = result.payment_method
        self.assertEqual(PayPalAccount, created_account.__class__)
        self.assertEqual("jane.doe@paypal.com", created_account.email)
        self.assertNotEqual(created_account.image_url, None)

        found_account = PaymentMethod.find(result.payment_method.token)
        self.assertNotEqual(None, found_account)
        self.assertEqual(created_account.token, found_account.token)
        self.assertEqual(created_account.customer_id, found_account.customer_id)

    def test_create_with_paypal_order_payment_nonce_and_paypal_options(self):
        customer_id = Customer.create().customer.id

        http = ClientApiHttp.create()
        status_code, payment_method_nonce = http.get_paypal_nonce({
            "intent": "order",
            "payment-token": "fake-paypal-payment-token",
            "payer-id": "fake-paypal-payer-id"
        })

        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": payment_method_nonce,
            "options": {
                "paypal": {
                    "payee_email": "payee@example.com",
                    "order_id": "merchant-order-id",
                    "custom_field": "custom merchant field",
                    "description": "merchant description",
                    "amount": "1.23",
                    "shipping": {
                        "first_name": "Andrew",
                        "last_name": "Mason",
                        "company": "Braintree",
                        "street_address": "456 W Main St",
                        "extended_address": "Apt 2F",
                        "locality": "Bartlett",
                        "region": "IL",
                        "postal_code": "60103",
                        "country_name": "Mexico",
                        "country_code_alpha2": "MX",
                        "country_code_alpha3": "MEX",
                        "country_code_numeric": "484"
                    },
                },
            },
        })

        self.assertTrue(result.is_success)
        created_account = result.payment_method
        self.assertEqual(PayPalAccount, created_account.__class__)
        self.assertEqual("bt_buyer_us@paypal.com", created_account.email)
        self.assertNotEqual(created_account.image_url, None)
        self.assertNotEqual(created_account.payer_id, None)

        found_account = PaymentMethod.find(result.payment_method.token)
        self.assertNotEqual(None, found_account)
        self.assertEqual(created_account.token, found_account.token)
        self.assertEqual(created_account.customer_id, found_account.customer_id)
        self.assertEqual(created_account.payer_id, found_account.payer_id)

    def test_create_with_paypal_refresh_token(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "paypal_refresh_token": "PAYPAL_REFRESH_TOKEN",
        })

        self.assertTrue(result.is_success)
        created_account = result.payment_method
        self.assertEqual(PayPalAccount, created_account.__class__)
        self.assertEqual("B_FAKE_ID", created_account.billing_agreement_id)
        self.assertNotEqual(created_account.payer_id, None)

        found_account = PaymentMethod.find(result.payment_method.token)
        self.assertNotEqual(None, found_account)
        self.assertEqual(created_account.token, found_account.token)
        self.assertEqual(created_account.customer_id, found_account.customer_id)
        self.assertEqual(created_account.billing_agreement_id, found_account.billing_agreement_id)
        self.assertEqual(created_account.payer_id, found_account.payer_id)

    def test_create_returns_validation_failures(self):
        http = ClientApiHttp.create()
        status_code, nonce = http.get_paypal_nonce({
            "options": {"validate": False}
        })
        self.assertEqual(202, status_code)
        result = PaymentMethod.create({
            "payment_method_nonce": nonce
        })

        self.assertFalse(result.is_success)
        paypal_error_codes = [
            error.code for error in result.errors.for_object("paypal_account").on("base")
        ]
        self.assertTrue(ErrorCodes.PayPalAccount.ConsentCodeOrAccessTokenIsRequired in paypal_error_codes)
        customer_error_codes = [
            error.code for error in result.errors.for_object("paypal_account").on("customer_id")
        ]
        self.assertTrue(ErrorCodes.PayPalAccount.CustomerIdIsRequiredForVaulting in customer_error_codes)

    def test_create_and_make_default(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "customer_id": customer_id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
        })
        self.assertTrue(credit_card_result.is_success)

        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.PayPalFuturePayment,
            "options": {"make_default": True},
        })

        self.assertTrue(result.is_success)
        self.assertTrue(result.payment_method.default)

    def test_create_and_set_token(self):
        customer_id = Customer.create().customer.id
        token = str(random.randint(1, 1000000))

        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.PayPalFuturePayment,
            "token": token
        })

        self.assertTrue(result.is_success)
        self.assertEqual(token, result.payment_method.token)

    def test_create_with_paypal_one_time_nonce_fails(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.PayPalOneTimePayment
        })

        self.assertFalse(result.is_success)
        base_errors = result.errors.for_object("paypal_account").on("base")
        self.assertEqual(1, len(base_errors))
        self.assertEqual(ErrorCodes.PayPalAccount.CannotVaultOneTimeUsePayPalAccount, base_errors[0].code)

    def test_create_with_credit_card_nonce(self):
        http = ClientApiHttp.create()
        status_code, nonce = http.get_credit_card_nonce({
            "number": "4111111111111111",
            "expirationMonth": "12",
            "expirationYear": "2020",
            "options": {"validate": False}
        })
        self.assertEqual(202, status_code)

        customer_id = Customer.create().customer.id

        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": nonce
        })

        self.assertTrue(result.is_success)
        created_credit_card = result.payment_method
        self.assertEqual(CreditCard, created_credit_card.__class__)
        self.assertEqual("411111", created_credit_card.bin)

        found_credit_card = PaymentMethod.find(result.payment_method.token)
        self.assertNotEqual(None, found_credit_card)
        self.assertEqual(found_credit_card.token, created_credit_card.token)
        self.assertEqual(found_credit_card.customer_id, created_credit_card.customer_id)

    def test_create_with_fake_apple_pay_nonce(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.ApplePayMasterCard
        })

        self.assertTrue(result.is_success)
        apple_pay_card = result.payment_method
        self.assertIsInstance(apple_pay_card, ApplePayCard)
        self.assertNotEqual(apple_pay_card.bin, None)
        self.assertNotEqual(apple_pay_card.card_type, None)
        self.assertNotEqual(apple_pay_card.commercial, None)
        self.assertNotEqual(apple_pay_card.country_of_issuance, None)
        self.assertNotEqual(apple_pay_card.debit, None)
        self.assertNotEqual(apple_pay_card.durbin_regulated, None)
        self.assertNotEqual(apple_pay_card.healthcare, None)
        self.assertNotEqual(apple_pay_card.issuing_bank, None)
        self.assertNotEqual(apple_pay_card.last_4, None)
        self.assertNotEqual(apple_pay_card.payroll, None)
        self.assertNotEqual(apple_pay_card.prepaid, None)
        self.assertNotEqual(apple_pay_card.prepaid_reloadable, None)
        self.assertNotEqual(apple_pay_card.product_id, None)
        self.assertNotEqual(apple_pay_card.token, None)

        self.assertEqual(apple_pay_card.customer_id, customer_id)
        self.assertEqual(ApplePayCard.CardType.MasterCard, apple_pay_card.card_type)
        self.assertEqual("MasterCard 0017", apple_pay_card.payment_instrument_name)
        self.assertEqual("MasterCard 0017", apple_pay_card.source_description)
        self.assertTrue(apple_pay_card.default)
        self.assertIn("apple_pay", apple_pay_card.image_url)
        self.assertTrue(int(apple_pay_card.expiration_month) > 0)
        self.assertTrue(int(apple_pay_card.expiration_year) > 0)

    def test_create_with_fake_apple_pay_mpan_nonce(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.ApplePayMpan
        })

        self.assertTrue(result.is_success)
        apple_pay_card = result.payment_method
        self.assertIsInstance(apple_pay_card, ApplePayCard)
        self.assertNotEqual(apple_pay_card.bin, None)
        self.assertNotEqual(apple_pay_card.card_type, None)
        self.assertNotEqual(apple_pay_card.commercial, None)
        self.assertNotEqual(apple_pay_card.country_of_issuance, None)
        self.assertNotEqual(apple_pay_card.debit, None)
        self.assertNotEqual(apple_pay_card.durbin_regulated, None)
        self.assertNotEqual(apple_pay_card.healthcare, None)
        self.assertNotEqual(apple_pay_card.issuing_bank, None)
        self.assertNotEqual(apple_pay_card.last_4, None)
        self.assertNotEqual(apple_pay_card.merchant_token_identifier, None)
        self.assertNotEqual(apple_pay_card.payroll, None)
        self.assertNotEqual(apple_pay_card.prepaid, None)
        self.assertNotEqual(apple_pay_card.prepaid_reloadable, None)
        self.assertNotEqual(apple_pay_card.product_id, None)
        self.assertNotEqual(apple_pay_card.source_card_last4, None)
        self.assertNotEqual(apple_pay_card.token, None)

        self.assertEqual(apple_pay_card.customer_id, customer_id)
        self.assertEqual(ApplePayCard.CardType.Visa, apple_pay_card.card_type)
        self.assertEqual("Visa 8886", apple_pay_card.payment_instrument_name)
        self.assertEqual("Visa 8886", apple_pay_card.source_description)
        self.assertTrue(apple_pay_card.default)
        self.assertIn("apple_pay", apple_pay_card.image_url)
        self.assertTrue(int(apple_pay_card.expiration_month) > 0)
        self.assertTrue(int(apple_pay_card.expiration_year) > 0)

    def test_create_with_fake_android_pay_proxy_card_nonce(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.AndroidPayCardDiscover
        })

        self.assertTrue(result.is_success)
        android_pay_card = result.payment_method
        self.assertIsInstance(android_pay_card, AndroidPayCard)
        self.assertNotEqual(android_pay_card.token, None)
        self.assertEqual(customer_id, android_pay_card.customer_id)
        self.assertEqual(CreditCard.CardType.Discover, android_pay_card.virtual_card_type)
        self.assertEqual("1117", android_pay_card.virtual_card_last_4)
        self.assertEqual("Discover 1111", android_pay_card.source_description)
        self.assertEqual(CreditCard.CardType.Discover, android_pay_card.source_card_type)
        self.assertEqual("1111", android_pay_card.source_card_last_4)
        self.assertEqual("1117", android_pay_card.last_4)
        self.assertEqual(CreditCard.CardType.Discover, android_pay_card.card_type)
        self.assertTrue(android_pay_card.default)
        self.assertIn("android_pay", android_pay_card.image_url)
        self.assertTrue(int(android_pay_card.expiration_month) > 0)
        self.assertTrue(int(android_pay_card.expiration_year) > 0)
        self.assertIsInstance(android_pay_card.created_at, datetime)
        self.assertIsInstance(android_pay_card.updated_at, datetime)
        self.assertEqual("601111", android_pay_card.bin)
        self.assertEqual("google_transaction_id", android_pay_card.google_transaction_id)
        self.assertFalse(android_pay_card.is_network_tokenized)

    def test_create_with_fake_android_pay_network_token_nonce(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.AndroidPayCardMasterCard
        })

        self.assertTrue(result.is_success)
        android_pay_card = result.payment_method
        self.assertIsInstance(android_pay_card, AndroidPayCard)
        self.assertNotEqual(android_pay_card.token, None)
        self.assertEqual(customer_id, android_pay_card.customer_id)
        self.assertEqual(CreditCard.CardType.MasterCard, android_pay_card.virtual_card_type)
        self.assertEqual("4444", android_pay_card.virtual_card_last_4)
        self.assertEqual("MasterCard 4444", android_pay_card.source_description)
        self.assertEqual(CreditCard.CardType.MasterCard, android_pay_card.source_card_type)
        self.assertEqual("4444", android_pay_card.source_card_last_4)
        self.assertEqual("4444", android_pay_card.last_4)
        self.assertEqual(CreditCard.CardType.MasterCard, android_pay_card.card_type)
        self.assertTrue(android_pay_card.default)
        self.assertIn("android_pay", android_pay_card.image_url)
        self.assertTrue(int(android_pay_card.expiration_month) > 0)
        self.assertTrue(int(android_pay_card.expiration_year) > 0)
        self.assertIsInstance(android_pay_card.created_at, datetime)
        self.assertIsInstance(android_pay_card.updated_at, datetime)
        self.assertEqual("555555", android_pay_card.bin)
        self.assertEqual("google_transaction_id", android_pay_card.google_transaction_id)
        self.assertTrue(android_pay_card.is_network_tokenized)
        self.assertNotEqual(android_pay_card.bin, None)
        self.assertNotEqual(android_pay_card.card_type, None)
        self.assertNotEqual(android_pay_card.commercial, None)
        self.assertNotEqual(android_pay_card.country_of_issuance, None)
        self.assertNotEqual(android_pay_card.debit, None)
        self.assertNotEqual(android_pay_card.durbin_regulated, None)
        self.assertNotEqual(android_pay_card.healthcare, None)
        self.assertNotEqual(android_pay_card.issuing_bank, None)
        self.assertNotEqual(android_pay_card.last_4, None)
        self.assertNotEqual(android_pay_card.payroll, None)
        self.assertNotEqual(android_pay_card.prepaid, None)
        self.assertNotEqual(android_pay_card.prepaid_reloadable, None)
        self.assertNotEqual(android_pay_card.product_id, None)
        self.assertNotEqual(android_pay_card.token, None)

    def test_create_with_fake_amex_express_checkout_card_nonce(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.AmexExpressCheckoutCard
        })

        self.assertTrue(result.is_success)
        amex_express_checkout_card = result.payment_method
        self.assertIsInstance(amex_express_checkout_card, AmexExpressCheckoutCard)
        self.assertNotEqual(amex_express_checkout_card.token, None)
        self.assertTrue(amex_express_checkout_card.default)
        self.assertEqual("American Express", amex_express_checkout_card.card_type)
        self.assertRegex(amex_express_checkout_card.bin, r"\A\d{6}\Z")
        self.assertRegex(amex_express_checkout_card.expiration_month, r"\A\d{2}\Z")
        self.assertRegex(amex_express_checkout_card.expiration_year, r"\A\d{4}\Z")
        self.assertRegex(amex_express_checkout_card.card_member_number, r"\A\d{4}\Z")
        self.assertRegex(amex_express_checkout_card.card_member_expiry_date, r"\A\d{2}/\d{2}\Z")
        self.assertRegex(amex_express_checkout_card.source_description, r"\AAmEx \d{4}\Z")
        self.assertRegex(amex_express_checkout_card.image_url, r"\.png")
        self.assertEqual(customer_id, amex_express_checkout_card.customer_id)

    def test_create_with_venmo_account_nonce(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.VenmoAccount,
        })

        self.assertTrue(result.is_success)
        venmo_account = result.payment_method
        self.assertIsInstance(venmo_account, VenmoAccount)

        self.assertTrue(venmo_account.default)
        self.assertIsNotNone(venmo_account.token)
        self.assertEqual("venmojoe", venmo_account.username)
        self.assertEqual("1234567891234567891", venmo_account.venmo_user_id)
        self.assertEqual("Venmo Account: venmojoe", venmo_account.source_description)
        self.assertRegex(venmo_account.image_url, r"\.png")
        self.assertEqual(customer_id, venmo_account.customer_id)

    def test_create_with_abstract_payment_method_nonce(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.AbstractTransactable
        })

        self.assertTrue(result.is_success)
        payment_method = result.payment_method
        self.assertNotEqual(None, payment_method)
        self.assertNotEqual(None, payment_method.token)
        self.assertEqual(customer_id, payment_method.customer_id)

    def test_create_with_custom_card_verification_amount(self):
        config = Configuration.instantiate()
        customer_id = Customer.create().customer.id
        client_token = json.loads(TestHelper.generate_decoded_client_token())
        authorization_fingerprint = client_token["authorizationFingerprint"]
        http = ClientApiHttp(config, {
                    "authorization_fingerprint": authorization_fingerprint,
                    "shared_customer_identifier": "fake_identifier",
                    "shared_customer_identifier_type": "testing"
                })
        status_code, nonce = http.get_credit_card_nonce({
            "number": "4000111111111115",
            "expirationMonth": "11",
            "expirationYear": "2099"
        })
        self.assertTrue(status_code == 201)

        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": nonce,
            "options": {
                "verify_card": "true",
                "verification_amount": "1.02"
            }
        })

        self.assertFalse(result.is_success)
        verification = result.credit_card_verification
        self.assertEqual(CreditCardVerification.Status.ProcessorDeclined, verification.status)

    def test_create_respects_verify_card_and_verification_merchant_account_id_when_outside_nonce(self):
        config = Configuration.instantiate()
        customer_id = Customer.create().customer.id
        client_token = json.loads(TestHelper.generate_decoded_client_token())
        authorization_fingerprint = client_token["authorizationFingerprint"]
        http = ClientApiHttp(config, {
                    "authorization_fingerprint": authorization_fingerprint,
                    "shared_customer_identifier": "fake_identifier",
                    "shared_customer_identifier_type": "testing"
                })
        status_code, nonce = http.get_credit_card_nonce({
            "number": "4000111111111115",
            "expirationMonth": "11",
            "expirationYear": "2099"
        })
        self.assertTrue(status_code == 201)

        result = PaymentMethod.create({
            "payment_method_nonce": nonce,
            "customer_id": customer_id,
            "options": {
                "verify_card": "true",
                "verification_merchant_account_id": TestHelper.non_default_merchant_account_id
            }
        })

        self.assertFalse(result.is_success)
        self.assertTrue(result.credit_card_verification.status == Transaction.Status.ProcessorDeclined)
        self.assertTrue(result.credit_card_verification.processor_response_code == "2000")
        self.assertTrue(result.credit_card_verification.processor_response_text == "Do Not Honor")
        self.assertTrue(result.credit_card_verification.merchant_account_id == TestHelper.non_default_merchant_account_id)

    def test_create_includes_risk_data_when_skip_advanced_fraud_checking_is_false(self):
        with FraudProtectionEnterpriseIntegrationMerchant():
            config = Configuration.instantiate()
            customer_id = Customer.create().customer.id
            client_token = json.loads(TestHelper.generate_decoded_client_token())
            authorization_fingerprint = client_token["authorizationFingerprint"]
            http = ClientApiHttp(config, {
                "authorization_fingerprint": authorization_fingerprint,
                "shared_customer_identifier": "fake_identifier",
                "shared_customer_identifier_type": "testing",
                })
            status_code, nonce = http.get_credit_card_nonce({
                "number": "4111111111111111",
                "expirationMonth": "11",
                "expirationYear": "2099",
                })
            self.assertTrue(status_code == 201)

            result = PaymentMethod.create({
                "customer_id": customer_id,
                "payment_method_nonce": nonce,
                "options": {
                    "verify_card": True,
                    "skip_advanced_fraud_checking": False
                    },
                })

            self.assertTrue(result.is_success)
            verification = result.payment_method.verification
            self.assertIsInstance(verification.risk_data, RiskData)

    def test_create_does_not_include_risk_data_when_skip_advanced_fraud_checking_is_true(self):
        with FraudProtectionEnterpriseIntegrationMerchant():
            config = Configuration.instantiate()
            customer_id = Customer.create().customer.id
            client_token = json.loads(TestHelper.generate_decoded_client_token())
            authorization_fingerprint = client_token["authorizationFingerprint"]
            http = ClientApiHttp(config, {
                "authorization_fingerprint": authorization_fingerprint,
                "shared_customer_identifier": "fake_identifier",
                "shared_customer_identifier_type": "testing",
                })
            status_code, nonce = http.get_credit_card_nonce({
                "number": "4111111111111111",
                "expirationMonth": "11",
                "expirationYear": "2099",
                })
            self.assertTrue(status_code == 201)

            result = PaymentMethod.create({
                "customer_id": customer_id,
                "payment_method_nonce": nonce,
                "options": {
                    "verify_card": True,
                    "skip_advanced_fraud_checking": True
                    },
                })

            self.assertTrue(result.is_success)
            verification = result.payment_method.verification
            self.assertIsNone(verification.risk_data)

    def test_create_respects_fail_one_duplicate_payment_method_when_included_outside_of_the_nonce(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "customer_id": customer_id,
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2012"
        })
        self.assertTrue(credit_card_result.is_success)

        config = Configuration.instantiate()
        customer_id = Customer.create().customer.id
        client_token = json.loads(TestHelper.generate_decoded_client_token())
        authorization_fingerprint = client_token["authorizationFingerprint"]
        http = ClientApiHttp(config, {
                    "authorization_fingerprint": authorization_fingerprint,
                    "shared_customer_identifier": "fake_identifier",
                    "shared_customer_identifier_type": "testing"
                })
        status_code, nonce = http.get_credit_card_nonce({
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2012"
        })
        self.assertTrue(status_code == 201)

        result = PaymentMethod.create({
            "payment_method_nonce": nonce,
            "customer_id": customer_id,
            "options": {
                "fail_on_duplicate_payment_method": "true"
            }
        })

        self.assertFalse(result.is_success)
        self.assertTrue(result.errors.deep_errors[0].code == "81724")

    def test_create_respects_fail_on_duplicate_payment_method_for_customer_when_included_outside_of_the_nonce(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "customer_id": customer_id,
            "number": "4111111111111111",
            "expiration_date": "05/2012"
        })
        self.assertTrue(credit_card_result.is_success)

        config = Configuration.instantiate()
        client_token = json.loads(TestHelper.generate_decoded_client_token())
        authorization_fingerprint = client_token["authorizationFingerprint"]
        http = ClientApiHttp(config, {
                    "authorization_fingerprint": authorization_fingerprint,
                    "shared_customer_identifier": "fake_identifier",
                    "shared_customer_identifier_type": "testing"
                })
        status_code, nonce = http.get_credit_card_nonce({
            "number": "4111111111111111",
            "expiration_date": "05/2014"
        })
        self.assertTrue(status_code == 201)

        result = PaymentMethod.create({
            "payment_method_nonce": nonce,
            "customer_id": customer_id,
            "options": {
                "fail_on_duplicate_payment_method_for_customer": "true"
            }
        })

        self.assertFalse(result.is_success)
        self.assertTrue(result.errors.deep_errors[0].code == "81763")

    def test_create_allows_passing_billing_address_id_outside_the_nonce(self):
        customer_id = Customer.create().customer.id
        http = ClientApiHttp.create()
        status_code, nonce = http.get_credit_card_nonce({
            "number": "4111111111111111",
            "expirationMonth": "12",
            "expirationYear": "2020",
            "options": {"validate": "false"}
        })
        self.assertTrue(status_code == 202)

        address_result = Address.create({
            "customer_id": customer_id,
            "first_name": "Bobby",
            "last_name": "Tables"
        })
        self.assertTrue(address_result.is_success)

        payment_method_result = PaymentMethod.create({
            "payment_method_nonce": nonce,
            "customer_id": customer_id,
            "billing_address_id": address_result.address.id
        })

        self.assertTrue(payment_method_result.is_success)
        self.assertTrue(isinstance(payment_method_result.payment_method, CreditCard))
        token = payment_method_result.payment_method.token

        found_credit_card = CreditCard.find(token)
        self.assertFalse(found_credit_card is None)
        self.assertTrue(found_credit_card.billing_address.first_name == "Bobby")
        self.assertTrue(found_credit_card.billing_address.last_name == "Tables")

    def test_create_allows_passing_billing_address_outside_the_nonce(self):
        customer_id = Customer.create().customer.id
        http = ClientApiHttp.create()
        status_code, nonce = http.get_credit_card_nonce({
            "number": "4111111111111111",
            "expirationMonth": "12",
            "expirationYear": "2020",
            "options": {"validate": "false"}
        })
        self.assertTrue(status_code == 202)

        result = PaymentMethod.create({
            "payment_method_nonce": nonce,
            "customer_id": customer_id,
            "billing_address": {
                "street_address": "123 Abc Way",
                "international_phone": {"country_code": "1", "national_number": "3121234567"}
            }
        })

        self.assertTrue(result.is_success)
        self.assertTrue(isinstance(result.payment_method, CreditCard))
        token = result.payment_method.token

        found_credit_card = CreditCard.find(token)
        self.assertFalse(found_credit_card is None)
        self.assertTrue(found_credit_card.billing_address.street_address == "123 Abc Way")
        self.assertEqual("1", found_credit_card.billing_address.international_phone["country_code"])
        self.assertEqual("3121234567", found_credit_card.billing_address.international_phone["national_number"])

    def test_create_overrides_the_billing_address_in_the_nonce(self):
        customer_id = Customer.create().customer.id
        http = ClientApiHttp.create()
        status_code, nonce = http.get_credit_card_nonce({
            "number": "4111111111111111",
            "expirationMonth": "12",
            "expirationYear": "2020",
            "options": {"validate": "false"},
            "billing_address": {
                "street_address": "456 Xyz Way"
            }
        })
        self.assertTrue(status_code == 202)

        result = PaymentMethod.create({
            "payment_method_nonce": nonce,
            "customer_id": customer_id,
            "billing_address": {
                "street_address": "123 Abc Way"
            }
        })

        self.assertTrue(result.is_success)
        self.assertTrue(isinstance(result.payment_method, CreditCard))
        token = result.payment_method.token

        found_credit_card = CreditCard.find(token)
        self.assertFalse(found_credit_card is None)
        self.assertTrue(found_credit_card.billing_address.street_address == "123 Abc Way")

    def test_create_does_not_override_the_billing_address_for_a_valuted_credit_card(self):
        config = Configuration.instantiate()
        customer_id = Customer.create().customer.id
        client_token = json.loads(TestHelper.generate_decoded_client_token({"customer_id": customer_id}))
        authorization_fingerprint = client_token["authorizationFingerprint"]
        http = ClientApiHttp(config, {"authorization_fingerprint": authorization_fingerprint})
        status_code, nonce = http.get_credit_card_nonce({
            "number": "4111111111111111",
            "expirationMonth": "12",
            "expirationYear": "2020",
            "billing_address": {
                "street_address": "456 Xyz Way"
            }
        })
        self.assertTrue(status_code == 201)

        result = PaymentMethod.create({
            "payment_method_nonce": nonce,
            "customer_id": customer_id,
            "billing_address": {
                "street_address": "123 Abc Way"
            }
        })

        self.assertTrue(result.is_success)
        self.assertTrue(isinstance(result.payment_method, CreditCard))
        token = result.payment_method.token

        found_credit_card = CreditCard.find(token)
        self.assertFalse(found_credit_card is None)
        self.assertTrue(found_credit_card.billing_address.street_address == "456 Xyz Way")

    def test_create_does_not_return_an_error_if_credit_card_options_are_present_for_paypal_nonce(self):
        customer_id = Customer.create().customer.id
        original_token = "paypal-account-" + str(int(time.time()))
        nonce = TestHelper.nonce_for_paypal_account({
            "consent_code": "consent-code",
            "token": original_token
        })

        result = PaymentMethod.create({
            "payment_method_nonce": nonce,
            "customer_id": customer_id,
            "options": {
                "verify_card": "true",
                "fail_on_duplicate_payment_method": "true",
                "fail_on_duplicate_payment_method_for_customer": "true",
                "verification_merchant_account_id": "not_a_real_merchant_account_id"
            }
        })

        self.assertTrue(result.is_success)

    def test_create_for_paypal_ignores_passed_billing_address_id(self):
        nonce = TestHelper.nonce_for_paypal_account({
            "consent_code": "consent-code"
        })
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "payment_method_nonce": nonce,
            "customer_id": customer_id,
            "billing_address_id": "address_id"
        })

        self.assertTrue(result.is_success)
        self.assertTrue(isinstance(result.payment_method, PayPalAccount))
        self.assertFalse(result.payment_method.image_url is None)
        token = result.payment_method.token

        found_paypal_account = PayPalAccount.find(token)
        self.assertFalse(found_paypal_account is None)

    def test_create_for_paypal_ignores_passed_billing_address_params(self):
        nonce = TestHelper.nonce_for_paypal_account({
            "consent_code": "PAYPAL_CONSENT_CODE"
        })
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "payment_method_nonce": nonce,
            "customer_id": customer_id,
            "billing_address": {
                "street_address": "123 Abc Way"
            }
        })

        self.assertTrue(result.is_success)
        self.assertTrue(isinstance(result.payment_method, PayPalAccount))
        self.assertFalse(result.payment_method.image_url is None)
        token = result.payment_method.token

        found_paypal_account = PayPalAccount.find(token)
        self.assertFalse(found_paypal_account is None)

    def test_create_payment_method_with_account_type_debit(self):
        config = Configuration.instantiate()
        customer_id = Customer.create().customer.id
        client_token = json.loads(TestHelper.generate_decoded_client_token())
        authorization_fingerprint = client_token["authorizationFingerprint"]
        http = ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing",
        })
        status_code, nonce = http.get_credit_card_nonce({
            "number": CreditCardNumbers.Hiper,
            "expirationMonth": "11",
            "expirationYear": "2099",
        })
        self.assertTrue(status_code == 201)

        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": nonce,
            "options": {
                "verify_card": "true",
                "verification_merchant_account_id": TestHelper.card_processor_brl_merchant_account_id,
                "verification_amount": "1.02",
                "verification_account_type": "debit",
            },
        })

        self.assertTrue(result.is_success)
        self.assertEqual("debit", result.payment_method.verifications[0]["credit_card"]["account_type"])

    def test_create_payment_method_with_account_type_credit(self):
        config = Configuration.instantiate()
        customer_id = Customer.create().customer.id
        client_token = json.loads(TestHelper.generate_decoded_client_token())
        authorization_fingerprint = client_token["authorizationFingerprint"]
        http = ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing",
        })
        status_code, nonce = http.get_credit_card_nonce({
            "number": CreditCardNumbers.Hiper,
            "expirationMonth": "11",
            "expirationYear": "2099",
        })
        self.assertTrue(status_code == 201)

        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": nonce,
            "options": {
                "verify_card": "true",
                "verification_merchant_account_id": TestHelper.hiper_brl_merchant_account_id,
                "verification_amount": "1.02",
                "verification_account_type": "credit",
            },
        })

        self.assertTrue(result.is_success)
        self.assertEqual("credit", result.payment_method.verifications[0]["credit_card"]["account_type"])

    def test_create_credit_card_with_account_type_debit(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.Hiper,
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe",
            "options": {
                "verification_merchant_account_id": TestHelper.card_processor_brl_merchant_account_id,
                "verification_account_type": "debit",
                "verify_card": True,
            }
        })
        self.assertTrue(result.is_success)
        self.assertEqual("debit", result.credit_card.verifications[0]["credit_card"]["account_type"])

    def test_create_credit_card_with_account_type_credit(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.Hiper,
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe",
            "options": {
                "verification_merchant_account_id": TestHelper.hiper_brl_merchant_account_id,
                "verification_account_type": "credit",
                "verify_card": True,
            }
        })
        self.assertTrue(result.is_success)
        self.assertEqual("credit", result.credit_card.verifications[0]["credit_card"]["account_type"])

    def test_create_with_usupported_merchant_account(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe",
            "options": {
                "verification_account_type": "debit",
                "verify_card": True,
            }
        })
        self.assertFalse(result.is_success)

        errors = result.errors.for_object("credit_card").for_object("options").on("verification_account_type")

        self.assertEqual(1, len(errors))
        self.assertEqual(ErrorCodes.CreditCard.VerificationAccountTypeNotSupported, errors[0].code)

    def test_create_with_invalid_account_type(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.Hiper,
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe",
            "options": {
                "verification_merchant_account_id": TestHelper.hiper_brl_merchant_account_id,
                "verification_account_type": "invalid",
                "verify_card": True,
            }
        })
        self.assertFalse(result.is_success)

        errors = result.errors.for_object("credit_card").for_object("options").on("verification_account_type")

        self.assertEqual(1, len(errors))
        self.assertEqual(ErrorCodes.CreditCard.VerificationAccountTypeIsInvald, errors[0].code)

    def test_find_returns_an_abstract_payment_method(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.AbstractTransactable
        })
        self.assertTrue(result.is_success)

        found_payment_method = PaymentMethod.find(result.payment_method.token)
        self.assertNotEqual(None, found_payment_method)
        self.assertEqual(found_payment_method.token, result.payment_method.token)

    def test_find_returns_a_paypal_account(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.PayPalFuturePayment
        })
        self.assertTrue(result.is_success)

        found_account = PaymentMethod.find(result.payment_method.token)
        self.assertNotEqual(None, found_account)
        self.assertEqual(PayPalAccount, found_account.__class__)
        self.assertTrue(found_account.email)

    def test_find_returns_a_credit_card(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })
        self.assertTrue(result.is_success)

        found_credit_card = PaymentMethod.find(result.credit_card.token)
        self.assertNotEqual(None, found_credit_card)
        self.assertEqual(CreditCard, found_credit_card.__class__)
        self.assertEqual("411111", found_credit_card.bin)

    def test_find_returns_an_android_pay_card(self):
        customer = Customer.create().customer
        result = PaymentMethod.create({
            "customer_id": customer.id,
            "payment_method_nonce": Nonces.AndroidPayCard
        })

        self.assertTrue(result.is_success)
        android_pay_card = result.payment_method

        found_android_pay_card = PaymentMethod.find(android_pay_card.token)
        self.assertNotEqual(None, found_android_pay_card)
        self.assertEqual(AndroidPayCard, found_android_pay_card.__class__)
        self.assertEqual(found_android_pay_card.token, android_pay_card.token)

    def test_find_returns_an_apple_pay_mpan_card(self):
        customer = Customer.create().customer
        result = PaymentMethod.create({
            "customer_id": customer.id,
            "payment_method_nonce": Nonces.ApplePayMpan
        })

        self.assertTrue(result.is_success)
        apple_pay_card = result.payment_method

        found_apple_pay_card = PaymentMethod.find(apple_pay_card.token)
        self.assertIsNotNone(found_apple_pay_card)
        self.assertEqual(ApplePayCard, found_apple_pay_card.__class__)
        self.assertEqual(found_apple_pay_card.token, apple_pay_card.token)
        self.assertEqual(apple_pay_card.merchant_token_identifier, "DNITHE302308980427388297")
        self.assertEqual(apple_pay_card.source_card_last4, "2006")
         

    def test_delete_customer_with_path_traversal(self):
        try:
            customer = Customer.create({"first_name":"Waldo"}).customer
            PaymentMethod.delete("../../customers/{}".format(customer.id))
        except NotFoundError:
            pass

        found_customer = Customer.find(customer.id)
        self.assertNotEqual(None, found_customer)
        self.assertEqual("Waldo", found_customer.first_name)

    def test_delete_deletes_a_credit_card(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })
        self.assertTrue(result.is_success)

        delete_result = PaymentMethod.delete(result.credit_card.token)
        self.assertTrue(delete_result.is_success)
        self.assertRaises(NotFoundError, PaymentMethod.find, result.credit_card.token)

    def test_delete_deletes_a_paypal_account(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.PayPalFuturePayment
        })
        self.assertTrue(result.is_success)

        delete_result = PaymentMethod.delete(result.payment_method.token, {"revoke_all_grants": False})
        self.assertTrue(delete_result.is_success)
        self.assertRaises(NotFoundError, PaymentMethod.find, result.payment_method.token)

    def test_update_credit_cards_updates_the_credit_card(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "cardholder_name": "Original Holder",
            "customer_id": customer_id,
            "cvv": "123",
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2012"
        })
        update_result = PaymentMethod.update(credit_card_result.credit_card.token, {
            "cardholder_name": "New Holder",
            "cvv": "456",
            "number": CreditCardNumbers.MasterCard,
            "expiration_date": "06/2013"
        })
        self.assertTrue(update_result.is_success)
        self.assertTrue(update_result.payment_method.token == credit_card_result.credit_card.token)
        updated_credit_card = update_result.payment_method
        self.assertTrue(updated_credit_card.bin == CreditCardNumbers.MasterCard[:6])
        self.assertTrue(updated_credit_card.last_4 == CreditCardNumbers.MasterCard[-4:])
        self.assertTrue(updated_credit_card.expiration_date == "06/2013")

    def test_update_with_three_d_secure_pass_thru(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "cardholder_name": "Original Holder",
            "customer_id": customer_id,
            "cvv": "123",
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2012"
        })
        update_result = PaymentMethod.update(credit_card_result.credit_card.token, {
            "cardholder_name": "New Holder",
            "cvv": "456",
            "number": CreditCardNumbers.MasterCard,
            "expiration_date": "06/2013",
            "three_d_secure_pass_thru": {
                "three_d_secure_version": "1.1.0",
                "eci_flag": "05",
                "cavv": "some-cavv",
                "xid": "some-xid"
            },
            "options": {
                "verify_card": "true",
            }
        })

        self.assertTrue(update_result.is_success)

    def test_create_with_three_d_secure_pass_thru_without_eci_flag(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "cardholder_name": "Original Holder",
            "customer_id": customer_id,
            "cvv": "123",
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2012"
        })
        update_result = PaymentMethod.update(credit_card_result.credit_card.token, {
            "cardholder_name": "New Holder",
            "cvv": "456",
            "number": CreditCardNumbers.MasterCard,
            "expiration_date": "06/2013",
            "three_d_secure_pass_thru": {
                "three_d_secure_version": "1.1.0",
                "cavv": "some-cavv",
                "xid": "some-xid"
            },
            "options": {
                "verify_card": "true",
            }
        })

        self.assertFalse(update_result.is_success)
        self.assertEqual("EciFlag is required.", update_result.message)

    def test_update_credit_cards_with_account_type_credit(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe",
        })
        update_result = PaymentMethod.update(result.credit_card.token, {
            "cardholder_name": "New Holder",
            "cvv": "456",
            "number": CreditCardNumbers.Hiper,
            "expiration_date": "06/2013",
            "options": {
                "verification_merchant_account_id": TestHelper.hiper_brl_merchant_account_id,
                "verification_account_type": "credit",
                "verify_card": True,
            }
        })
        self.assertTrue(update_result.is_success)
        self.assertEqual("credit", update_result.payment_method.verification.credit_card["account_type"])

    def test_update_credit_cards_with_account_type_debit(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe",
        })
        update_result = PaymentMethod.update(result.credit_card.token, {
            "cardholder_name": "New Holder",
            "cvv": "456",
            "number": CreditCardNumbers.Hiper,
            "expiration_date": "06/2013",
            "options": {
                "verification_merchant_account_id": TestHelper.card_processor_brl_merchant_account_id,
                "verification_account_type": "debit",
                "verify_card": True,
            }
        })
        self.assertTrue(update_result.is_success)
        self.assertEqual("debit", update_result.payment_method.verification.credit_card["account_type"])

    def test_update_credit_cards_with_invalid_account_type(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe",
        })
        update_result = PaymentMethod.update(result.credit_card.token, {
            "cardholder_name": "New Holder",
            "cvv": "456",
            "number": CreditCardNumbers.Hiper,
            "expiration_date": "06/2013",
            "options": {
                "verification_merchant_account_id": TestHelper.hiper_brl_merchant_account_id,
                "verification_account_type": "invalid",
                "verify_card": True,
            }
        })
        self.assertFalse(update_result.is_success)
        errors = update_result.errors.for_object("credit_card").for_object("options").on("verification_account_type")
        self.assertEqual(1, len(errors))
        self.assertEqual(ErrorCodes.CreditCard.VerificationAccountTypeIsInvald, errors[0].code)

    def test_update_credit_cards_with_unsupported_merchant_account(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe",
        })
        update_result = PaymentMethod.update(result.credit_card.token, {
            "cardholder_name": "New Holder",
            "cvv": "456",
            "number": CreditCardNumbers.Visa,
            "expiration_date": "06/2013",
            "options": {
                "verification_account_type": "debit",
                "verify_card": True,
            }
        })
        self.assertFalse(update_result.is_success)
        errors = update_result.errors.for_object("credit_card").for_object("options").on("verification_account_type")
        self.assertEqual(1, len(errors))
        self.assertEqual(ErrorCodes.CreditCard.VerificationAccountTypeNotSupported, errors[0].code)

    def test_update_creates_a_new_billing_address_by_default(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "customer_id": customer_id,
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2012",
            "billing_address": {
                "street_address": "123 Nigeria Ave"
            }
        })
        update_result = PaymentMethod.update(credit_card_result.credit_card.token, {
            "billing_address": {
                "region": "IL",
                "international_phone": {"country_code": "1", "national_number": "3121234567"}
            }
        })
        self.assertTrue(update_result.is_success)
        updated_credit_card = update_result.payment_method
        self.assertTrue(updated_credit_card.billing_address.region == "IL")
        self.assertEqual("1", updated_credit_card.billing_address.international_phone["country_code"])
        self.assertEqual("3121234567", updated_credit_card.billing_address.international_phone["national_number"])
        self.assertTrue(updated_credit_card.billing_address.street_address is None)
        self.assertFalse(updated_credit_card.billing_address.id == credit_card_result.credit_card.billing_address.id)

    def test_update_updates_the_billing_address_if_option_is_specified(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "customer_id": customer_id,
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2012",
            "billing_address": {
                "street_address": "123 Nigeria Ave"
            }
        })
        update_result = PaymentMethod.update(credit_card_result.credit_card.token, {
            "billing_address": {
                "region": "IL",
                "options": {
                    "update_existing": "true"
                }
            }
        })
        self.assertTrue(update_result.is_success)
        updated_credit_card = update_result.payment_method
        self.assertTrue(updated_credit_card.billing_address.region == "IL")
        self.assertTrue(updated_credit_card.billing_address.street_address == "123 Nigeria Ave")
        self.assertTrue(updated_credit_card.billing_address.id == credit_card_result.credit_card.billing_address.id)

    def test_update_updates_the_country_via_codes(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "customer_id": customer_id,
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2012",
            "billing_address": {
                "street_address": "123 Nigeria Ave"
            }
        })
        update_result = PaymentMethod.update(credit_card_result.credit_card.token, {
            "billing_address": {
                "country_name": "American Samoa",
                "country_code_alpha2": "AS",
                "country_code_alpha3": "ASM",
                "country_code_numeric": "016",
                "options": {
                    "update_existing": "true"
                }
            }
        })
        self.assertTrue(update_result.is_success)
        updated_credit_card = update_result.payment_method
        self.assertTrue(updated_credit_card.billing_address.country_name == "American Samoa")
        self.assertTrue(updated_credit_card.billing_address.country_code_alpha2 == "AS")
        self.assertTrue(updated_credit_card.billing_address.country_code_alpha3 == "ASM")
        self.assertTrue(updated_credit_card.billing_address.country_code_numeric == "016")

    def test_update_can_pass_expiration_month_and_expiration_year(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "customer_id": customer_id,
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2012"
        })
        update_result = PaymentMethod.update(credit_card_result.credit_card.token, {
            "number": CreditCardNumbers.MasterCard,
            "expiration_month": "07",
            "expiration_year": "2011"
        })
        self.assertTrue(update_result.is_success)
        self.assertTrue(update_result.payment_method.token == credit_card_result.credit_card.token)
        updated_credit_card = update_result.payment_method
        self.assertTrue(updated_credit_card.expiration_month == "07")
        self.assertTrue(updated_credit_card.expiration_year == "2011")
        self.assertTrue(updated_credit_card.expiration_date == "07/2011")

    def test_update_verifies_the_update_if_options_verify_card_is_true(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "cardholder_name": "Original Holder",
            "customer_id": customer_id,
            "cvv": "123",
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2012"
        })
        update_result = PaymentMethod.update(credit_card_result.credit_card.token, {
            "cardholder_name": "New Holder",
            "cvv": "456",
            "number": CreditCardNumbers.FailsSandboxVerification.MasterCard,
            "expiration_date": "06/2013",
            "options": {
                "verify_card": "true"
            }
        })
        self.assertFalse(update_result.is_success)
        self.assertTrue(update_result.credit_card_verification.status == CreditCardVerification.Status.ProcessorDeclined)
        self.assertTrue(update_result.credit_card_verification.gateway_rejection_reason is None)

    def test_update_can_pass_custom_verification_amount(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "cardholder_name": "Card Holder",
            "customer_id": customer_id,
            "cvv": "123",
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2020"
        })
        update_result = PaymentMethod.update(credit_card_result.credit_card.token, {
            "payment_method_nonce": Nonces.ProcessorDeclinedMasterCard,
            "options": {
                "verify_card": "true",
                "verification_amount": "2.34"
            }
        })
        self.assertFalse(update_result.is_success)
        self.assertTrue(update_result.credit_card_verification.status == CreditCardVerification.Status.ProcessorDeclined)
        self.assertTrue(update_result.credit_card_verification.gateway_rejection_reason is None)

    def test_update_includes_risk_data_when_skip_advanced_fraud_checking_is_false(self):
        with FraudProtectionEnterpriseIntegrationMerchant():
            customer_id = Customer.create().customer.id
            credit_card_result = CreditCard.create({
                "cardholder_name": "Card Holder",
                "customer_id": customer_id,
                "cvv": "123",
                "number": "4111111111111111",
                "expiration_date": "05/2020"
            })

            update_result = PaymentMethod.update(credit_card_result.credit_card.token, {
                "expiration_date": "10/2020",
                "options": {
                    "verify_card": True,
                    "skip_advanced_fraud_checking": False
                    },
                })

            self.assertTrue(update_result.is_success)
            verification = update_result.payment_method.verification
            self.assertIsInstance(verification.risk_data, RiskData)

    def test_update_does_not_include_risk_data_when_skip_advanced_fraud_checking_is_true(self):
        with FraudProtectionEnterpriseIntegrationMerchant():
            customer_id = Customer.create().customer.id
            credit_card_result = CreditCard.create({
                "cardholder_name": "Card Holder",
                "customer_id": customer_id,
                "cvv": "123",
                "number": "4111111111111111",
                "expiration_date": "05/2020"
            })

            update_result = PaymentMethod.update(credit_card_result.credit_card.token, {
                "expiration_date": "10/2020",
                "options": {
                    "verify_card": True,
                    "skip_advanced_fraud_checking": True
                    },
                })

            self.assertTrue(update_result.is_success)
            verification = update_result.payment_method.verification
            self.assertIsNone(verification.risk_data)

    def test_update_can_update_the_billing_address(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "cardholder_name": "Original Holder",
            "customer_id": customer_id,
            "cvv": "123",
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2012",
            "billing_address": {
                "first_name": "Old First Name",
                "last_name": "Old Last Name",
                "company": "Old Company",
                "street_address": "123 Old St",
                "extended_address": "Apt Old",
                "locality": "Old City",
                "region": "Old State",
                "postal_code": "12345",
                "country_name": "Canada"
            }
        })
        update_result = PaymentMethod.update(credit_card_result.credit_card.token, {
            "options": {"verify_card": "false"},
            "billing_address": {
                "first_name": "New First Name",
                "last_name": "New Last Name",
                "company": "New Company",
                "street_address": "123 New St",
                "extended_address": "Apt New",
                "locality": "New City",
                "region": "New State",
                "postal_code": "56789",
                "country_name": "United States of America"
            }
        })
        self.assertTrue(update_result.is_success)
        address = update_result.payment_method.billing_address
        self.assertTrue(address.first_name == "New First Name")
        self.assertTrue(address.last_name == "New Last Name")
        self.assertTrue(address.company == "New Company")
        self.assertTrue(address.street_address == "123 New St")
        self.assertTrue(address.extended_address == "Apt New")
        self.assertTrue(address.locality == "New City")
        self.assertTrue(address.region == "New State")
        self.assertTrue(address.postal_code == "56789")
        self.assertTrue(address.country_name == "United States of America")

    def test_update_returns_an_error_response_if_invalid(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "cardholder_name": "Original Holder",
            "customer_id": customer_id,
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2012"
        })
        update_result = PaymentMethod.update(credit_card_result.credit_card.token, {
            "cardholder_name": "New Holder",
            "number": "invalid",
            "expiration_date": "05/2014",
        })
        self.assertFalse(update_result.is_success)

        number_errors = update_result.errors.for_object("credit_card").on("number")
        self.assertEqual(1, len(number_errors))
        self.assertEqual("Credit card number must be 12-19 digits.", number_errors[0].message)

    def test_update_can_update_the_default(self):
        customer_id = Customer.create().customer.id
        card1 = CreditCard.create({
            "customer_id": customer_id,
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2009"
        }).credit_card
        card2 = CreditCard.create({
            "customer_id": customer_id,
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2009"
        }).credit_card

        self.assertTrue(card1.default)
        self.assertFalse(card2.default)

        PaymentMethod.update(card2.token, {
            "options": {"make_default": True}
        })

        self.assertFalse(CreditCard.find(card1.token).default)
        self.assertTrue(CreditCard.find(card2.token).default)

    def test_update_updates_a_paypal_accounts_token(self):
        customer_id = Customer.create().customer.id
        original_token = "paypal-account-" + str(int(time.time()))
        nonce = TestHelper.nonce_for_paypal_account({
            "consent_code": "consent-code",
            "token": original_token
        })
        original_result = PaymentMethod.create({
             "payment_method_nonce": nonce,
             "customer_id": customer_id
        })

        updated_token = "UPDATED_TOKEN-" + str(random.randint(0, 100000000))
        PaymentMethod.update(
            original_token,
            {"token": updated_token}
        )

        updated_paypal_account = PayPalAccount.find(updated_token)
        self.assertTrue(updated_paypal_account.email == original_result.payment_method.email)
        self.assertRaises(NotFoundError, PaymentMethod.find, original_token)

    def test_update_can_make_a_paypal_account_the_default_payment_method(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "customer_id": customer_id,
            "number": CreditCardNumbers.Visa,
            "expiration_date": "05/2009",
            "options": {"make_default": "true"}
        })
        self.assertTrue(credit_card_result.is_success)

        nonce = TestHelper.nonce_for_paypal_account({
            "consent_code": "consent-code"
        })
        original_token = PaymentMethod.create({
             "payment_method_nonce": nonce,
             "customer_id": customer_id
        }).payment_method.token

        PaymentMethod.update(
            original_token,
            {"options": {"make_default": "true"}}
        )

        updated_paypal_account = PayPalAccount.find(original_token)
        self.assertTrue(updated_paypal_account.default)

    def test_update_fails_to_updates_a_paypal_accounts_token_with(self):
        customer_id = Customer.create().customer.id
        first_token = "paypal-account-" + str(random.randint(0, 100000000))
        second_token = "paypal-account-" + str(random.randint(0, 100000000))

        first_nonce = TestHelper.nonce_for_paypal_account({
            "consent_code": "consent-code",
            "token": first_token
        })
        PaymentMethod.create({
             "payment_method_nonce": first_nonce,
             "customer_id": customer_id
        })

        second_nonce = TestHelper.nonce_for_paypal_account({
            "consent_code": "consent-code",
            "token": second_token
        })
        PaymentMethod.create({
             "payment_method_nonce": second_nonce,
             "customer_id": customer_id
        })

        updated_result = PaymentMethod.update(
            first_token,
            {"token": second_token}
        )

        self.assertFalse(updated_result.is_success)

        errors = updated_result.errors.deep_errors
        self.assertEqual(1, len(errors))
        self.assertEqual("92906", errors[0].code)

    def test_update_respects_fail_on_duplicate_payment_method_for_customer_when_included_outside_of_the_nonce(self):
        customer_id = Customer.create().customer.id
        credit_card_result = CreditCard.create({
            "customer_id": customer_id,
            "number": "4111111111111111",
            "expiration_date": "05/2012"
        })
        self.assertTrue(credit_card_result.is_success)

        credit_card_result_2 = CreditCard.create({
            "customer_id": customer_id,
            "number": "4000111111111115",
            "expiration_date": "05/2012"
        })
        self.assertTrue(credit_card_result_2.is_success)

        update_result = PaymentMethod.update(credit_card_result_2.credit_card.token, {
            "cardholder_name": "New Holder",
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "options": {
                "fail_on_duplicate_payment_method_for_customer": "true"
            }
        })
        self.assertFalse(update_result.is_success)
        self.assertTrue(update_result.errors.deep_errors[0].code == "81763")

    def test_payment_method_grant_raises_on_non_existent_tokens(self):
        granting_gateway, _ = TestHelper.create_payment_method_grant_fixtures()
        self.assertRaises(NotFoundError, granting_gateway.payment_method.grant, "non-existant-token", False)

    def test_payment_method_grant_returns_one_time_nonce(self):
        """
        Payment method grant returns a nonce that is transactable by a partner merchant exactly once
        """
        granting_gateway, credit_card = TestHelper.create_payment_method_grant_fixtures()
        grant_result = granting_gateway.payment_method.grant(credit_card.token, { "allow_vaulting": False });
        self.assertTrue(grant_result.is_success)

        result = Transaction.sale({
            "payment_method_nonce": grant_result.payment_method_nonce.nonce,
            "amount": TransactionAmounts.Authorize
        })
        self.assertTrue(result.is_success)
        result = Transaction.sale({
            "payment_method_nonce": grant_result.payment_method_nonce.nonce,
            "amount": TransactionAmounts.Authorize
        })
        self.assertFalse(result.is_success)

    def test_payment_method_grant_returns_a_nonce_that_is_not_vaultable(self):
        granting_gateway, credit_card = TestHelper.create_payment_method_grant_fixtures()
        grant_result = granting_gateway.payment_method.grant(credit_card.token, False)
        customer_id = Customer.create().customer.id

        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": grant_result.payment_method_nonce.nonce
        })
        self.assertFalse(result.is_success)

    def test_payment_method_grant_returns_a_nonce_that_is_vaultable(self):
        granting_gateway, credit_card = TestHelper.create_payment_method_grant_fixtures()
        grant_result = granting_gateway.payment_method.grant(credit_card.token, { "allow_vaulting": True })
        customer_id = Customer.create().customer.id

        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": grant_result.payment_method_nonce.nonce
        })
        self.assertTrue(result.is_success)

    def test_payment_method_revoke_renders_a_granted_nonce_unusable(self):
        granting_gateway, credit_card = TestHelper.create_payment_method_grant_fixtures()
        grant_result = granting_gateway.payment_method.grant(credit_card.token)

        revoke_result = granting_gateway.payment_method.revoke(credit_card.token)
        self.assertTrue(revoke_result.is_success)

        result = Transaction.sale({
            "payment_method_nonce": grant_result.payment_method_nonce.nonce,
            "amount": TransactionAmounts.Authorize
        })
        self.assertFalse(result.is_success)

    def test_payment_method_revoke_raises_on_non_existent_tokens(self):
        granting_gateway, _ = TestHelper.create_payment_method_grant_fixtures()
        self.assertRaises(NotFoundError, granting_gateway.payment_method.revoke, "non-existant-token")

    def test_vault_sepa_direct_debit_payment_method_with_fake_nonce(self):
        customer_id = Customer.create().customer.id

        result = PaymentMethod.create({
            "payment_method_nonce": Nonces.SepaDirectDebit,
            "customer_id": customer_id,
        })

        self.assertTrue(result.is_success)

    def test_delete_sepa_direct_debit_payment_method(self):
        customer_id = Customer.create().customer.id

        result = PaymentMethod.create({
            "payment_method_nonce": Nonces.SepaDirectDebit,
            "customer_id": customer_id,
        })

        self.assertTrue(result.is_success)

        delete_result = PaymentMethod.delete(result.payment_method.token)

        self.assertRaises(NotFoundError, PaymentMethod.find, result.payment_method.token)
