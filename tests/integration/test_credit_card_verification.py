from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers

class TestCreditCardVerfication(unittest.TestCase):

    def test_create_success(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "cardholder_name": "John Smith",
                "expiration_date": "05/2012"
        }})

        self.assertTrue(result.is_success)
        verification = result.verification
        self.assertEqual("1000", verification.processor_response_code)
        self.assertEqual(ProcessorResponseTypes.Approved, verification.processor_response_type)

    def test_create_failure(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.FailsSandboxVerification.MasterCard,
                "expiration_date": "05/2012"
        }})

        self.assertFalse(result.is_success)
        verification = result.credit_card_verification
        self.assertEqual("2000", verification.processor_response_code)
        self.assertEqual(ProcessorResponseTypes.SoftDeclined, verification.processor_response_type)

    def test_create_returns_validation_errors(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.FailsSandboxVerification.MasterCard,
                "expiration_date": "05/2012"
            },
            "options": {"amount": "-10.00"}
        })

        self.assertFalse(result.is_success)

        amount_errors = result.errors.for_object("verification").for_object("options").on("amount")
        self.assertEqual(1, len(amount_errors))
        self.assertEqual(ErrorCodes.Verification.Options.AmountCannotBeNegative, amount_errors[0].code)

    def test_create_with_account_type_debit(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.Hiper,
                "expiration_date": "10/2020",
                "cvv": "737",
            },
            "options": {
                "merchant_account_id": TestHelper.card_processor_brl_merchant_account_id,
                "account_type": "debit",
            },
        })

        self.assertTrue(result.is_success)
        self.assertEqual("debit", result.verification.credit_card["account_type"])

    def test_create_with_account_type_credit(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.Hiper,
                "expiration_date": "10/2020",
                "cvv": "737",
            },
            "options": {
                "merchant_account_id": TestHelper.hiper_brl_merchant_account_id,
                "account_type": "credit",
            },
        })

        self.assertTrue(result.is_success)
        self.assertEqual("credit", result.verification.credit_card["account_type"])


    def test_create_with_unsupported_account_type(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "cardholder_name": "John Smith",
                "expiration_date": "05/2012"
            },
            "options": {
                "account_type": "debit",
            },
        })

        self.assertFalse(result.is_success)

        account_type_errors = result.errors.for_object("verification").for_object("options").on("account_type")
        self.assertEqual(1, len(account_type_errors))
        self.assertEqual(ErrorCodes.Verification.Options.AccountTypeNotSupported , account_type_errors[0].code)

    def test_create_with_invalid_account_type(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.Hiper,
                "expiration_date": "10/2020",
                "cvv": "737",
            },
            "options": {
                "merchant_account_id": TestHelper.hiper_brl_merchant_account_id,
                "account_type": "invalid",
            },
        })

        self.assertFalse(result.is_success)

        account_type_errors = result.errors.for_object("verification").for_object("options").on("account_type")
        self.assertEqual(1, len(account_type_errors))
        self.assertEqual(ErrorCodes.Verification.Options.AccountTypeIsInvalid, account_type_errors[0].code)

    def test_create_with_external_vault(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "cardholder_name": "John Smith",
                "expiration_date": "05/2012"
            },
            "external_vault": {
                "status": "will_vault"
            }
            })

        self.assertTrue(result.is_success)
        verification = result.verification
        self.assertEqual("1000", verification.processor_response_code)
        self.assertEqual(ProcessorResponseTypes.Approved, verification.processor_response_type)

    def test_create_with_risk_data(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "cardholder_name": "John Smith",
                "expiration_date": "05/2012"
            },
            "risk_data": {
                "customer_browser": "IE7",
                "customer_ip": "192.168.0.1"
            }
        })

        self.assertTrue(result.is_success)
        verification = result.verification
        self.assertEqual("1000", verification.processor_response_code)
        self.assertEqual(ProcessorResponseTypes.Approved, verification.processor_response_type)

    def test_find_with_verification_id(self):
        customer = Customer.create({
            "credit_card": {
                "number": CreditCardNumbers.FailsSandboxVerification.MasterCard,
                "expiration_date": "05/2012",
                "cardholder_name": "Tom Smith",
                "options": {"verify_card": True}
        }})

        created_verification = customer.credit_card_verification
        found_verification = CreditCardVerification.find(created_verification.id)
        self.assertEqual(created_verification, found_verification)
        self.assertNotEqual(None, found_verification.graphql_id)

    def test_verification_not_found(self):
        self.assertRaises(NotFoundError, CreditCardVerification.find,
          "invalid-id")

    def test_card_type_indicators(self):
        cardholder_name = "Tom %s" % random.randint(1, 10000)
        Customer.create({"credit_card": {
            "cardholder_name": cardholder_name,
            "expiration_date": "10/2012",
            "number": CreditCardNumbers.CardTypeIndicators.Unknown,
            "options": {"verify_card": True}
        }})
        found_verifications = CreditCardVerification.search(
            CreditCardVerificationSearch.credit_card_cardholder_name == cardholder_name
        )

        self.assertEqual(CreditCard.Commercial.Unknown, found_verifications.first.credit_card['commercial'])
        self.assertEqual(CreditCard.CountryOfIssuance.Unknown, found_verifications.first.credit_card['country_of_issuance'])
        self.assertEqual(CreditCard.Debit.Unknown, found_verifications.first.credit_card['debit'])
        self.assertEqual(CreditCard.DurbinRegulated.Unknown, found_verifications.first.credit_card['durbin_regulated'])
        self.assertEqual(CreditCard.Healthcare.Unknown, found_verifications.first.credit_card['healthcare'])
        self.assertEqual(CreditCard.IssuingBank.Unknown, found_verifications.first.credit_card['issuing_bank'])
        self.assertEqual(CreditCard.Payroll.Unknown, found_verifications.first.credit_card['payroll'])
        self.assertEqual(CreditCard.Prepaid.Unknown, found_verifications.first.credit_card['prepaid'])
        self.assertEqual(CreditCard.PrepaidReloadable.Unknown, found_verifications.first.credit_card['prepaid_reloadable'])
        self.assertEqual(CreditCard.ProductId.Unknown, found_verifications.first.credit_card['product_id'])

    def test_create_success_network_response_code_text(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "cardholder_name": "John Smith",
                "expiration_date": "05/2012"
            },
        })

        self.assertTrue(result.is_success)
        verification = result.verification
        self.assertEqual("1000", verification.processor_response_code)
        self.assertEqual(ProcessorResponseTypes.Approved, verification.processor_response_type)
        self.assertEqual("XX", verification.network_response_code)
        self.assertEqual("sample network response text", verification.network_response_text)

    def test_create_success_network_transaction_id(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "cardholder_name": "John Smith",
                "expiration_date": "05/2012"
            },
        })

        self.assertTrue(result.is_success)
        verification = result.verification
        self.assertRegex(verification.network_transaction_id, r'\d{15}')

    def test_verification_with_three_d_secure_authentication_id_with_nonce(self):
        config = Configuration(
                environment=Environment.Development,
                merchant_id="integration_merchant_id",
                public_key="integration_public_key",
                private_key="integration_private_key"
                )
        gateway = BraintreeGateway(config)
        credit_card = {
                "credit_card": {
                    "number": CreditCardNumbers.Visa,
                    "expiration_month": "05",
                    "expiration_year": "2029",
                    }
                }
        nonce = TestHelper.generate_three_d_secure_nonce(gateway, credit_card)
        found_nonce = PaymentMethodNonce.find(nonce)
        three_d_secure_info = found_nonce.three_d_secure_info

        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "cardholder_name": "John Smith",
                },
            "options": {"merchant_account_id": TestHelper.three_d_secure_merchant_account_id},
            "payment_method_nonce": nonce,
            "three_d_secure_authentication_id": three_d_secure_info.three_d_secure_authentication_id
            })

        self.assertTrue(result.is_success)
        verification = result.verification
        self.assertEqual("1000", verification.processor_response_code)
        self.assertEqual(ProcessorResponseTypes.Approved, verification.processor_response_type)

    def test_verification_with_three_d_secure_pass_thru(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "cardholder_name": "John Smith",
                "expiration_date": "05/2029"},
            "options": {"merchant_account_id": TestHelper.three_d_secure_merchant_account_id},
            "three_d_secure_pass_thru": {
                "eci_flag": "02",
                "cavv": "some_cavv",
                "xid": "some_xid",
                "three_d_secure_version": "1.0.2",
                "authentication_response": "Y",
                "directory_response": "Y",
                "cavv_algorithm": "2",
                "ds_transaction_id": "some_ds_id"}})

        self.assertTrue(result.is_success)
        verification = result.verification
        self.assertEqual("1000", verification.processor_response_code)
        self.assertEqual(ProcessorResponseTypes.Approved, verification.processor_response_type)

    def test_verification_with_intended_transaction_source(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "cardholder_name": "John Smith",
                "expiration_date": "05/2029"},
            "intended_transaction_source": "installment"
            })

        self.assertTrue(result.is_success)
        verification = result.verification
        self.assertEqual("1000", verification.processor_response_code)
        self.assertEqual(ProcessorResponseTypes.Approved, verification.processor_response_type)

    def test_verification_with_ani_response_codes(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2029",
            }
        })

        self.assertTrue(result.is_success)
        verification = result.verification
        self.assertEqual("1000", verification.processor_response_code)
        self.assertEqual("I", verification.ani_first_name_response_code)
        self.assertEqual("I", verification.ani_last_name_response_code)
