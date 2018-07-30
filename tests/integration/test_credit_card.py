from tests.test_helper import *
from braintree.test.credit_card_defaults import CreditCardDefaults
from braintree.test.credit_card_numbers import CreditCardNumbers
import braintree.test.venmo_sdk as venmo_sdk

class TestCreditCard(unittest.TestCase):
    def test_create_adds_credit_card_to_existing_customer(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertTrue(result.is_success)
        credit_card = result.credit_card
        self.assertTrue(re.search(r"\A\w{4,}\Z", credit_card.token) is not None)
        self.assertEqual("411111", credit_card.bin)
        self.assertEqual("1111", credit_card.last_4)
        self.assertEqual("05", credit_card.expiration_month)
        self.assertEqual("2014", credit_card.expiration_year)
        self.assertEqual("05/2014", credit_card.expiration_date)
        self.assertEqual("John Doe", credit_card.cardholder_name)
        self.assertNotEqual(re.search(r"\A\w{32}\Z", credit_card.unique_number_identifier), None)
        self.assertFalse(credit_card.venmo_sdk)
        self.assertNotEqual(re.search("png", credit_card.image_url), None)

    def test_create_and_make_default(self):
        customer = Customer.create().customer
        card1 = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        }).credit_card

        self.assertTrue(card1.default)

        card2 = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "cvv": "100",
            "cardholder_name": "John Doe",
            "options":
                {"make_default": True}
        }).credit_card

        card1 = CreditCard.find(card1.token)
        self.assertFalse(card1.default)
        self.assertTrue(card2.default)

    def test_create_with_expiration_month_and_year(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertTrue(result.is_success)
        credit_card = result.credit_card
        self.assertEqual("05/2014", credit_card.expiration_date)

    def test_create_with_security_params(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "2014",
            "cvv": "100",
            "cardholder_name": "John Doe",
            "device_session_id": "abc123",
            "fraud_merchant_id": "456"
        })

        self.assertTrue(result.is_success)

    def test_create_can_specify_the_desired_token(self):
        token = str(random.randint(1, 1000000))
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "token": token
        })

        self.assertTrue(result.is_success)
        credit_card = result.credit_card
        self.assertEqual(token, credit_card.token)

    def test_create_with_billing_address(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "billing_address": {
                "street_address": "123 Abc Way",
                "locality": "Chicago",
                "region": "Illinois",
                "postal_code": "60622",
                "country_code_alpha2": "MX",
                "country_code_alpha3": "MEX",
                "country_code_numeric": "484",
                "country_name": "Mexico"
            }
        })

        self.assertTrue(result.is_success)
        address = result.credit_card.billing_address
        self.assertEqual("123 Abc Way", address.street_address)
        self.assertEqual("Chicago", address.locality)
        self.assertEqual("Illinois", address.region)
        self.assertEqual("60622", address.postal_code)
        self.assertEqual("MX", address.country_code_alpha2)
        self.assertEqual("MEX", address.country_code_alpha3)
        self.assertEqual("484", address.country_code_numeric)
        self.assertEqual("Mexico", address.country_name)

    def test_create_with_billing_address_id(self):
        customer = Customer.create().customer
        address = Address.create({
            "customer_id": customer.id,
            "street_address": "123 Abc Way"
        }).address

        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "billing_address_id": address.id
        })

        self.assertTrue(result.is_success)
        billing_address = result.credit_card.billing_address
        self.assertEqual(address.id, billing_address.id)
        self.assertEqual("123 Abc Way", billing_address.street_address)

    def test_create_without_billing_address_still_has_billing_address_method(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
        })
        self.assertTrue(result.is_success)
        self.assertEqual(None, result.credit_card.billing_address)


    def test_unsuccessful_create_with_card_verification_returns_risk_data(self):
        with AdvancedFraudIntegrationMerchant():
            customer = Customer.create().customer
            result = CreditCard.create({
                "customer_id": customer.id,
                "number": "4000111111111115",
                "expiration_date": "05/2014",
                "options": {"verify_card": True},
                "device_session_id": "abc123"
            })

            self.assertFalse(result.is_success)
            verification = result.credit_card_verification
            self.assertIsInstance(verification.risk_data, RiskData)
            self.assertTrue(hasattr(verification.risk_data, 'id'))
            self.assertEqual("Approve", verification.risk_data.decision)
            self.assertTrue(hasattr(verification.risk_data, 'device_data_captured'))

    def test_successful_create_with_card_verification_returns_risk_data(self):
        with AdvancedFraudIntegrationMerchant():
            customer = Customer.create().customer
            result = CreditCard.create({
                "customer_id": customer.id,
                "number": "4111111111111111",
                "expiration_date": "05/2014",
                "options": {"verify_card": True},
                "device_session_id": "abc123"
            })

            self.assertTrue(result.is_success)
            verification = result.credit_card.verification
            self.assertIsInstance(verification.risk_data, RiskData)
            self.assertTrue(hasattr(verification.risk_data, 'id'))
            self.assertEqual("Approve", verification.risk_data.decision)
            self.assertTrue(hasattr(verification.risk_data, 'device_data_captured'))

    def test_create_with_card_verification(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4000111111111115",
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        self.assertFalse(result.is_success)
        verification = result.credit_card_verification
        self.assertEqual(CreditCardVerification.Status.ProcessorDeclined, verification.status)
        self.assertEqual("2000", verification.processor_response_code)
        self.assertEqual("Do Not Honor", verification.processor_response_text)
        self.assertEqual("I", verification.cvv_response_code)
        self.assertEqual(None, verification.avs_error_response_code)
        self.assertEqual("I", verification.avs_postal_code_response_code)
        self.assertEqual("I", verification.avs_street_address_response_code)
        self.assertEqual(Decimal("0.00"), verification.amount)
        self.assertEqual("USD", verification.currency_iso_code)
        self.assertEqual(TestHelper.default_merchant_account_id, verification.merchant_account_id)

    def test_create_with_card_verification_with_overridden_amount(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4000111111111115",
            "expiration_date": "05/2014",
            "options": {"verify_card": True, "verification_amount": "1.02"}
        })

        self.assertFalse(result.is_success)
        verification = result.credit_card_verification
        self.assertEqual(CreditCardVerification.Status.ProcessorDeclined, verification.status)
        self.assertEqual("2000", verification.processor_response_code)
        self.assertEqual("Do Not Honor", verification.processor_response_text)
        self.assertEqual("I", verification.cvv_response_code)
        self.assertEqual(None, verification.avs_error_response_code)
        self.assertEqual("I", verification.avs_postal_code_response_code)
        self.assertEqual("I", verification.avs_street_address_response_code)
        self.assertEqual(Decimal("1.02"), verification.amount)
        self.assertEqual("USD", verification.currency_iso_code)
        self.assertEqual(TestHelper.default_merchant_account_id, verification.merchant_account_id)

    def test_create_with_card_verification_and_non_default_merchant_account(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4000111111111115",
            "expiration_date": "05/2014",
            "options": {
                "verification_merchant_account_id": TestHelper.non_default_merchant_account_id,
                "verify_card": True
            }
        })

        self.assertFalse(result.is_success)
        verification = result.credit_card_verification
        self.assertEqual(CreditCardVerification.Status.ProcessorDeclined, verification.status)
        self.assertEqual(None, verification.gateway_rejection_reason)
        self.assertEqual(TestHelper.non_default_merchant_account_id, verification.merchant_account_id)

    def test_verify_gateway_rejected_responds_to_processor_response_code(self):
        old_merchant_id = Configuration.merchant_id
        old_public_key = Configuration.public_key
        old_private_key = Configuration.private_key

        try:
            Configuration.merchant_id = "processing_rules_merchant_id"
            Configuration.public_key = "processing_rules_public_key"
            Configuration.private_key = "processing_rules_private_key"

            customer = Customer.create().customer
            result = CreditCard.create({
                "customer_id": customer.id,
                "number": "4111111111111111",
                "expiration_date": "05/2014",
                "billing_address": {
                    "postal_code": "20000"
                },
                "options": {
                    "verify_card": True
                }
            })


            self.assertFalse(result.is_success)
            self.assertEqual('1000', result.credit_card_verification.processor_response_code)
            self.assertEqual('Approved', result.credit_card_verification.processor_response_text)
        finally:
            Configuration.merchant_id = old_merchant_id
            Configuration.public_key = old_public_key
            Configuration.private_key = old_private_key

    def test_expose_gateway_rejection_reason_on_verification(self):
        old_merchant_id = Configuration.merchant_id
        old_public_key = Configuration.public_key
        old_private_key = Configuration.private_key

        try:
            Configuration.merchant_id = "processing_rules_merchant_id"
            Configuration.public_key = "processing_rules_public_key"
            Configuration.private_key = "processing_rules_private_key"

            customer = Customer.create().customer
            result = CreditCard.create({
                "customer_id": customer.id,
                "number": "4111111111111111",
                "expiration_date": "05/2014",
                "cvv": "200",
                "options": {
                    "verify_card": True
                }
            })

            self.assertFalse(result.is_success)
            verification = result.credit_card_verification
            self.assertEqual(Transaction.GatewayRejectionReason.Cvv, verification.gateway_rejection_reason)
        finally:
            Configuration.merchant_id = old_merchant_id
            Configuration.public_key = old_public_key
            Configuration.private_key = old_private_key

    def test_create_with_card_verification_set_to_false(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4000111111111115",
            "expiration_date": "05/2014",
            "options": {"verify_card": False}
        })

        self.assertTrue(result.is_success)

    def test_create_with_fail_on_duplicate_payment_method_set_to_true(self):
        customer = Customer.create().customer
        CreditCard.create({
            "customer_id": customer.id,
            "number": "4000111111111115",
            "expiration_date": "05/2014"
        })

        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4000111111111115",
            "expiration_date": "05/2014",
            "options": {"fail_on_duplicate_payment_method": True}
        })

        self.assertFalse(result.is_success)
        self.assertEqual("Duplicate card exists in the vault.", result.message)

        credit_card_number_errors = result.errors.for_object("credit_card").on("number")
        self.assertEqual(1, len(credit_card_number_errors))
        self.assertEqual(ErrorCodes.CreditCard.DuplicateCardExists, credit_card_number_errors[0].code)

    def test_create_with_invalid_invalid_options(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "invalid_date",
        })

        self.assertFalse(result.is_success)
        self.assertEqual("Expiration date is invalid.", result.message)

        expiration_date_errors = result.errors.for_object("credit_card").on("expiration_date")
        self.assertEqual(1, len(expiration_date_errors))
        self.assertEqual(ErrorCodes.CreditCard.ExpirationDateIsInvalid, expiration_date_errors[0].code)

    def test_create_with_invalid_country_codes(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2012",
            "billing_address": {
                "country_code_alpha2": "ZZ",
                "country_code_alpha3": "ZZZ",
                "country_code_numeric": "000",
                "country_name": "zzzzzzz"
            }
        })

        self.assertFalse(result.is_success)

        country_code_alpha2_errors = result.errors.for_object("credit_card").for_object("billing_address").on("country_code_alpha2")
        self.assertEqual(1, len(country_code_alpha2_errors))
        self.assertEqual(ErrorCodes.Address.CountryCodeAlpha2IsNotAccepted, country_code_alpha2_errors[0].code)

        country_code_alpha3_errors = result.errors.for_object("credit_card").for_object("billing_address").on("country_code_alpha3")
        self.assertEqual(1, len(country_code_alpha3_errors))
        self.assertEqual(ErrorCodes.Address.CountryCodeAlpha3IsNotAccepted, country_code_alpha3_errors[0].code)

        country_code_numeric_errors = result.errors.for_object("credit_card").for_object("billing_address").on("country_code_numeric")
        self.assertEqual(1, len(country_code_numeric_errors))
        self.assertEqual(ErrorCodes.Address.CountryCodeNumericIsNotAccepted, country_code_numeric_errors[0].code)

        country_name_errors = result.errors.for_object("credit_card").for_object("billing_address").on("country_name")
        self.assertEqual(1, len(country_name_errors))
        self.assertEqual(ErrorCodes.Address.CountryNameIsNotAccepted, country_name_errors[0].code)

    def test_create_with_venmo_sdk_payment_method_code(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "venmo_sdk_payment_method_code": venmo_sdk.VisaPaymentMethodCode
        })

        self.assertTrue(result.is_success)
        self.assertEqual("411111", result.credit_card.bin)
        self.assertFalse(result.credit_card.venmo_sdk)

    def test_create_with_invalid_venmo_sdk_payment_method_code(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "venmo_sdk_payment_method_code": venmo_sdk.InvalidPaymentMethodCode
        })

        self.assertFalse(result.is_success)
        self.assertEqual("Invalid VenmoSDK payment method code", result.message)

        venmo_sdk_payment_method_code_errors = result.errors.for_object("credit_card").on("venmo_sdk_payment_method_code")
        self.assertEqual(1, len(venmo_sdk_payment_method_code_errors))
        self.assertEqual(ErrorCodes.CreditCard.InvalidVenmoSDKPaymentMethodCode, venmo_sdk_payment_method_code_errors[0].code)

    def test_create_with_payment_method_nonce(self):
        config = Configuration.instantiate()
        authorization_fingerprint = json.loads(TestHelper.generate_decoded_client_token())["authorizationFingerprint"]
        http = ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing"
        })
        _, response = http.add_card({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "11",
                "expiration_year": "2099",
            },
            "share": True
        })
        nonce = json.loads(response)["creditCards"][0]["nonce"]
        customer = Customer.create().customer

        result = CreditCard.create({
            "customer_id": customer.id,
            "payment_method_nonce": nonce
        })

        self.assertTrue(result.is_success)
        self.assertEqual("411111", result.credit_card.bin)

    def test_create_with_venmo_sdk_session(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "cvv": "100",
            "cardholder_name": "John Doe",
            "options": {
                "venmo_sdk_session": venmo_sdk.Session
            }
        })
        self.assertTrue(result.is_success)
        self.assertFalse(result.credit_card.venmo_sdk)

    def test_create_with_invalid_venmo_sdk_session(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "cvv": "100",
            "cardholder_name": "John Doe",
            "options": {
                "venmo_sdk_session": venmo_sdk.InvalidSession
            }
        })
        self.assertTrue(result.is_success)
        self.assertFalse(result.credit_card.venmo_sdk)

    def test_update_with_valid_options(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        }).credit_card

        result = CreditCard.update(credit_card.token, {
            "number": "5105105105105100",
            "expiration_date": "06/2010",
            "cvv": "123",
            "cardholder_name": "Jane Jones"
        })

        self.assertTrue(result.is_success)
        credit_card = result.credit_card
        self.assertTrue(re.search(r"\A\w{4,}\Z", credit_card.token) is not None)
        self.assertEqual("510510", credit_card.bin)
        self.assertEqual("5100", credit_card.last_4)
        self.assertEqual("06", credit_card.expiration_month)
        self.assertEqual("2010", credit_card.expiration_year)
        self.assertEqual("06/2010", credit_card.expiration_date)
        self.assertEqual("Jane Jones", credit_card.cardholder_name)

    def test_update_billing_address_creates_new_by_default(self):
        customer = Customer.create().customer
        initial_credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "billing_address": {
                "street_address": "123 Nigeria Ave",
            }
        }).credit_card

        updated_credit_card = CreditCard.update(initial_credit_card.token, {
            "billing_address": {
                "region": "IL",
                "country_code_alpha2": "NG",
                "country_code_alpha3": "NGA",
                "country_code_numeric": "566",
                "country_name": "Nigeria"
            }
        }).credit_card

        self.assertEqual("IL", updated_credit_card.billing_address.region)
        self.assertEqual("NG", updated_credit_card.billing_address.country_code_alpha2)
        self.assertEqual("NGA", updated_credit_card.billing_address.country_code_alpha3)
        self.assertEqual("566", updated_credit_card.billing_address.country_code_numeric)
        self.assertEqual("Nigeria", updated_credit_card.billing_address.country_name)
        self.assertEqual(None, updated_credit_card.billing_address.street_address)
        self.assertNotEqual(initial_credit_card.billing_address.id, updated_credit_card.billing_address.id)

    def test_update_billing_address_when_update_existing_is_True(self):
        customer = Customer.create().customer
        initial_credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "billing_address": {
                "street_address": "123 Nigeria Ave",
            }
        }).credit_card

        updated_credit_card = CreditCard.update(initial_credit_card.token, {
            "billing_address": {
                "region": "IL",
                "options": {
                    "update_existing": True
                }
            }
        }).credit_card

        self.assertEqual("IL", updated_credit_card.billing_address.region)
        self.assertEqual("123 Nigeria Ave", updated_credit_card.billing_address.street_address)
        self.assertEqual(initial_credit_card.billing_address.id, updated_credit_card.billing_address.id)

    def test_update_and_make_default(self):
        customer = Customer.create().customer
        card1 = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        }).credit_card
        card2 = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        }).credit_card

        self.assertTrue(card1.default)
        self.assertFalse(card2.default)

        CreditCard.update(card2.token, {
            "options": {
                "make_default": True
            }
        })
        self.assertFalse(CreditCard.find(card1.token).default)
        self.assertTrue(CreditCard.find(card2.token).default)


    def test_update_verifies_card_if_option_is_provided(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        }).credit_card

        result = CreditCard.update(credit_card.token, {
            "number": "4000111111111115",
            "expiration_date": "06/2010",
            "cvv": "123",
            "cardholder_name": "Jane Jones",
            "options": {"verify_card": True}
        })

        self.assertFalse(result.is_success)
        self.assertEqual(CreditCardVerification.Status.ProcessorDeclined, result.credit_card_verification.status)

    def test_update_verifies_card_with_non_default_merchant_account(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        }).credit_card

        result = CreditCard.update(credit_card.token, {
            "number": "4000111111111115",
            "expiration_date": "06/2010",
            "cvv": "123",
            "cardholder_name": "Jane Jones",
            "options": {
                "verification_merchant_account_id": TestHelper.non_default_merchant_account_id,
                "verify_card": True
            }
        })

        self.assertFalse(result.is_success)
        self.assertEqual(CreditCardVerification.Status.ProcessorDeclined, result.credit_card_verification.status)

    def test_update_billing_address(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "billing_address": {
                "street_address": "321 Xyz Way",
                "locality": "Chicago",
                "region": "Illinois",
                "postal_code": "60621"
            }
        }).credit_card

        result = CreditCard.update(credit_card.token, {
            "billing_address": {
                "street_address": "123 Abc Way",
                "locality": "Chicago",
                "region": "Illinois",
                "postal_code": "60622"
            }
        })

        self.assertTrue(result.is_success)
        address = result.credit_card.billing_address
        self.assertEqual("123 Abc Way", address.street_address)
        self.assertEqual("Chicago", address.locality)
        self.assertEqual("Illinois", address.region)
        self.assertEqual("60622", address.postal_code)

    def test_update_returns_error_if_invalid(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014"
        }).credit_card

        result = CreditCard.update(credit_card.token, {
            "expiration_date": "invalid_date"
        })

        self.assertFalse(result.is_success)

        expiration_date_errors = result.errors.for_object("credit_card").on("expiration_date")
        self.assertEqual(1, len(expiration_date_errors))
        self.assertEqual(ErrorCodes.CreditCard.ExpirationDateIsInvalid, expiration_date_errors[0].code)

    def test_update_returns_error_with_duplicate_payment_method_if_fail_on_duplicate_payment_method_is_set(self):
        create_result = Customer.create({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2021",
            }
        })
        self.assertTrue(create_result.is_success)

        update_result = Customer.update(create_result.customer.id, {
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2021",
                "options": {
                    "fail_on_duplicate_payment_method": True,
                },
            }
        })

        self.assertFalse(update_result.is_success)
        number_errors = update_result.errors.for_object("customer").for_object("credit_card").on("number")
        self.assertEqual(1, len(number_errors))
        self.assertEqual(ErrorCodes.CreditCard.DuplicateCardExists, number_errors[0].code)

    def test_delete_with_valid_token(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014"
        }).credit_card

        result = CreditCard.delete(credit_card.token)
        self.assertTrue(result.is_success)

    @raises(NotFoundError)
    def test_delete_raises_error_when_deleting_twice(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014"
        }).credit_card

        CreditCard.delete(credit_card.token)
        CreditCard.delete(credit_card.token)

    @raises(NotFoundError)
    def test_delete_with_invalid_token(self):
        CreditCard.delete("notreal")

    def test_find_with_valid_token(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014"
        }).credit_card

        found_credit_card = CreditCard.find(credit_card.token)
        self.assertTrue(re.search(r"\A\w{4,}\Z", found_credit_card.token) is not None)
        self.assertEqual("411111", found_credit_card.bin)
        self.assertEqual("1111", found_credit_card.last_4)
        self.assertEqual("05", found_credit_card.expiration_month)
        self.assertEqual("2014", found_credit_card.expiration_year)
        self.assertEqual("05/2014", found_credit_card.expiration_date)

    def test_find_returns_associated_subsriptions(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014"
        }).credit_card
        subscription_id = "id_" + str(random.randint(1, 1000000))
        subscription = Subscription.create({
            "id": subscription_id,
            "plan_id": "integration_trialless_plan",
            "payment_method_token": credit_card.token,
            "price": Decimal("1.00")
        }).subscription

        found_credit_card = CreditCard.find(credit_card.token)
        subscriptions = found_credit_card.subscriptions

        self.assertEqual(1, len(subscriptions))
        subscription = subscriptions[0]

        self.assertEqual(subscription_id, subscription.id)
        self.assertEqual(Decimal("1.00"), subscription.price)
        self.assertEqual(credit_card.token, subscription.payment_method_token)

    @raises_with_regexp(NotFoundError, "payment method with token 'bad_token' not found")
    def test_find_with_invalid_token(self):
        CreditCard.find("bad_token")

    def test_from_nonce_with_unlocked_nonce(self):
        config = Configuration.instantiate()
        customer = Customer.create().customer

        client_token = TestHelper.generate_decoded_client_token({
            "customer_id": customer.id,
        })
        authorization_fingerprint = json.loads(client_token)["authorizationFingerprint"]
        http = ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing"
        })

        status_code, response = http.add_card({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(201, status_code)
        nonce = json.loads(response)["creditCards"][0]["nonce"]

        card = CreditCard.from_nonce(nonce)
        customer = Customer.find(customer.id)
        self.assertEqual(1, len(customer.credit_cards))
        self.assertEqual(customer.credit_cards[0].token, card.token)

    @raises_with_regexp(NotFoundError, "payment method with nonce .* or not found")
    def test_from_nonce_with_unlocked_nonce_pointing_to_shared_card(self):
        config = Configuration.instantiate()

        client_token = TestHelper.generate_decoded_client_token()
        authorization_fingerprint = json.loads(client_token)["authorizationFingerprint"]
        http = ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing"
        })

        status_code, response = http.add_card({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "11",
                "expiration_year": "2099",
            },
            "share": True
        })
        self.assertEqual(201, status_code)
        nonce = json.loads(response)["creditCards"][0]["nonce"]

        CreditCard.from_nonce(nonce)

    @raises_with_regexp(NotFoundError, ".* consumed .*")
    def test_from_nonce_with_consumed_nonce(self):
        config = Configuration.instantiate()
        customer = Customer.create().customer

        client_token = TestHelper.generate_decoded_client_token({
            "customer_id": customer.id,
        })
        authorization_fingerprint = json.loads(client_token)["authorizationFingerprint"]
        http = ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing"
        })

        status_code, response = http.add_card({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(201, status_code)
        nonce = json.loads(response)["creditCards"][0]["nonce"]

        CreditCard.from_nonce(nonce)
        CreditCard.from_nonce(nonce)

    def test_create_from_transparent_redirect(self):
        customer = Customer.create().customer
        tr_data = {
            "credit_card": {
                "customer_id": customer.id
            }
        }
        post_params = {
            "tr_data": CreditCard.tr_data_for_create(tr_data, "http://example.com/path?foo=bar"),
            "credit_card[cardholder_name]": "Card Holder",
            "credit_card[number]": "4111111111111111",
            "credit_card[expiration_date]": "05/2012",
            "credit_card[billing_address][country_code_alpha2]": "MX",
            "credit_card[billing_address][country_code_alpha3]": "MEX",
            "credit_card[billing_address][country_code_numeric]": "484",
            "credit_card[billing_address][country_name]": "Mexico",
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, CreditCard.transparent_redirect_create_url())
        result = CreditCard.confirm_transparent_redirect(query_string)
        self.assertTrue(result.is_success)
        credit_card = result.credit_card
        self.assertEqual("411111", credit_card.bin)
        self.assertEqual("1111", credit_card.last_4)
        self.assertEqual("05", credit_card.expiration_month)
        self.assertEqual("2012", credit_card.expiration_year)
        self.assertEqual(customer.id, credit_card.customer_id)
        self.assertEqual("MX", credit_card.billing_address.country_code_alpha2)
        self.assertEqual("MEX", credit_card.billing_address.country_code_alpha3)
        self.assertEqual("484", credit_card.billing_address.country_code_numeric)
        self.assertEqual("Mexico", credit_card.billing_address.country_name)


    def test_create_from_transparent_redirect_and_make_default(self):
        customer = Customer.create().customer
        card1 = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "cvv": "100",
            "cardholder_name": "John Doe"
        }).credit_card
        self.assertTrue(card1.default)

        tr_data = {
            "credit_card": {
                "customer_id": customer.id,
                "options": {
                    "make_default": True
                }
            }
        }
        post_params = {
            "tr_data": CreditCard.tr_data_for_create(tr_data, "http://example.com/path?foo=bar"),
            "credit_card[cardholder_name]": "Card Holder",
            "credit_card[number]": "4111111111111111",
            "credit_card[expiration_date]": "05/2012",
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, CreditCard.transparent_redirect_create_url())
        card2 = CreditCard.confirm_transparent_redirect(query_string).credit_card

        self.assertFalse(CreditCard.find(card1.token).default)
        self.assertTrue(card2.default)

    def test_create_from_transparent_redirect_with_error_result(self):
        customer = Customer.create().customer
        tr_data = {
            "credit_card": {
                "customer_id": customer.id
            }
        }

        post_params = {
            "tr_data": CreditCard.tr_data_for_create(tr_data, "http://example.com/path"),
            "credit_card[cardholder_name]": "Card Holder",
            "credit_card[number]": "eleventy",
            "credit_card[expiration_date]": "y2k"
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, CreditCard.transparent_redirect_create_url())
        result = CreditCard.confirm_transparent_redirect(query_string)
        self.assertFalse(result.is_success)

        credit_card_number_errors = result.errors.for_object("credit_card").on("number")
        self.assertEqual(1, len(credit_card_number_errors))
        self.assertEqual(ErrorCodes.CreditCard.NumberHasInvalidLength, credit_card_number_errors[0].code)

        expiration_date_errors = result.errors.for_object("credit_card").on("expiration_date")
        self.assertEqual(1, len(expiration_date_errors))
        self.assertEqual(ErrorCodes.CreditCard.ExpirationDateIsInvalid, expiration_date_errors[0].code)

    def test_update_from_transparent_redirect_with_successful_result(self):
        old_token = str(random.randint(1, 1000000))
        new_token = str(random.randint(1, 1000000))
        credit_card = Customer.create({
            "credit_card": {
                "cardholder_name": "Old Cardholder Name",
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "token": old_token
            }
        }).customer.credit_cards[0]

        tr_data = {
            "payment_method_token": old_token,
            "credit_card": {
                "token": new_token
            }
        }

        post_params = {
            "tr_data": CreditCard.tr_data_for_update(tr_data, "http://example.com/path"),
            "credit_card[cardholder_name]": "New Cardholder Name",
            "credit_card[expiration_date]": "05/2014"
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, CreditCard.transparent_redirect_update_url())
        result = CreditCard.confirm_transparent_redirect(query_string)
        self.assertTrue(result.is_success)
        credit_card = result.credit_card
        self.assertEqual(new_token, credit_card.token)
        self.assertEqual("411111", credit_card.bin)
        self.assertEqual("1111", credit_card.last_4)
        self.assertEqual("05", credit_card.expiration_month)
        self.assertEqual("2014", credit_card.expiration_year)

    def test_update_from_transparent_redirect_and_make_default(self):
        customer = Customer.create({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012"
            }
        }).customer
        card1 = customer.credit_cards[0]

        card2 = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
        }).credit_card

        self.assertTrue(card1.default)
        self.assertFalse(card2.default)

        tr_data = {
            "payment_method_token": card2.token,
            "credit_card": {
                "options": {
                    "make_default": True
                }
            }
        }

        post_params = {
            "tr_data": CreditCard.tr_data_for_update(tr_data, "http://example.com/path"),
            "credit_card[cardholder_name]": "New Cardholder Name",
            "credit_card[expiration_date]": "05/2014"
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, CreditCard.transparent_redirect_update_url())
        CreditCard.confirm_transparent_redirect(query_string)

        self.assertFalse(CreditCard.find(card1.token).default)
        self.assertTrue(CreditCard.find(card2.token).default)

    def test_update_from_transparent_redirect_and_update_existing_billing_address(self):
        customer = Customer.create({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "billing_address": {
                    "street_address": "123 Old St",
                    "locality": "Chicago",
                    "region": "Illinois",
                    "postal_code": "60621"
                }
            }
        }).customer
        card = customer.credit_cards[0]

        tr_data = {
            "payment_method_token": card.token,
            "credit_card": {
                "billing_address": {
                    "street_address": "123 New St",
                    "locality": "Columbus",
                    "region": "Ohio",
                    "postal_code": "43215",
                    "options": {
                        "update_existing": True
                    }
                }
            }
        }

        post_params = {
            "tr_data": CreditCard.tr_data_for_update(tr_data, "http://example.com/path")
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, CreditCard.transparent_redirect_update_url())

        CreditCard.confirm_transparent_redirect(query_string)

        self.assertEqual(1, len(Customer.find(customer.id).addresses))
        updated_card = CreditCard.find(card.token)
        self.assertEqual("123 New St", updated_card.billing_address.street_address)
        self.assertEqual("Columbus", updated_card.billing_address.locality)
        self.assertEqual("Ohio", updated_card.billing_address.region)
        self.assertEqual("43215", updated_card.billing_address.postal_code)

    def test_update_from_transparent_redirect_with_error_result(self):
        old_token = str(random.randint(1, 1000000))
        Customer.create({
            "credit_card": {
                "cardholder_name": "Old Cardholder Name",
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "token": old_token
            }
        })

        tr_data = {
            "payment_method_token": old_token,
            "credit_card": {
                "token": "bad token"
            }
        }

        post_params = {
            "tr_data": CreditCard.tr_data_for_update(tr_data, "http://example.com/path"),
            "credit_card[cardholder_name]": "New Cardholder Name",
            "credit_card[expiration_date]": "05/2014"
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, CreditCard.transparent_redirect_update_url())
        result = CreditCard.confirm_transparent_redirect(query_string)
        self.assertFalse(result.is_success)

        credit_card_token_errors = result.errors.for_object("credit_card").on("token")
        self.assertEqual(1, len(credit_card_token_errors))
        self.assertEqual(ErrorCodes.CreditCard.TokenInvalid, credit_card_token_errors[0].code)

    def test_expired_can_iterate_over_all_items(self):
        customer_id = Customer.all().first.id

        for _ in range(110 - CreditCard.expired().maximum_size):
            CreditCard.create({
                "customer_id": customer_id,
                "number": "4111111111111111",
                "expiration_date": "05/2014",
                "cvv": "100",
                "cardholder_name": "John Doe"
            })

        collection = CreditCard.expired()
        self.assertTrue(collection.maximum_size > 100)

        credit_card_tokens = [credit_card.token for credit_card in collection.items]
        self.assertEqual(collection.maximum_size, len(TestHelper.unique(credit_card_tokens)))

        self.assertEqual(set([True]), TestHelper.unique([credit_card.is_expired for credit_card in collection.items]))

    def test_expiring_between(self):
        customer_id = Customer.all().first.id

        for _ in range(110 - CreditCard.expiring_between(date(2010, 1, 1), date(2010, 12, 31)).maximum_size):
            CreditCard.create({
                "customer_id": customer_id,
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "cvv": "100",
                "cardholder_name": "John Doe"
            })

        collection = CreditCard.expiring_between(date(2010, 1, 1), date(2010, 12, 31))
        self.assertTrue(collection.maximum_size > 100)

        credit_card_tokens = [credit_card.token for credit_card in collection.items]
        self.assertEqual(collection.maximum_size, len(TestHelper.unique(credit_card_tokens)))

        self.assertEqual(set(['2010']), TestHelper.unique([credit_card.expiration_year for credit_card in collection.items]))

    def test_commercial_card(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.Commercial,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEqual(CreditCard.Commercial.Yes, credit_card.commercial)

    def test_issuing_bank(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.IssuingBank,
            "expiration_date": "05/2014"
        })

        credit_card = result.credit_card

        self.assertEqual(CreditCardDefaults.IssuingBank, credit_card.issuing_bank)

    def test_country_of_issuance(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.CountryOfIssuance,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEqual(CreditCardDefaults.CountryOfIssuance, credit_card.country_of_issuance)

    def test_durbin_regulated_card(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.DurbinRegulated,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEqual(CreditCard.DurbinRegulated.Yes, credit_card.durbin_regulated)

    def test_debit_card(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.Debit,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEqual(CreditCard.Debit.Yes, credit_card.debit)

    def test_healthcare_card(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.Healthcare,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEqual(CreditCard.Healthcare.Yes, credit_card.healthcare)
        self.assertEqual("J3", credit_card.product_id)

    def test_payroll_card(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.Payroll,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEqual(CreditCard.Payroll.Yes, credit_card.payroll)
        self.assertEqual("MSA", credit_card.product_id)

    def test_prepaid_card(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.Prepaid,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEqual(CreditCard.Prepaid.Yes, credit_card.prepaid)

    def test_all_negative_card_type_indicators(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.No,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEqual(CreditCard.Debit.No, credit_card.debit)
        self.assertEqual(CreditCard.DurbinRegulated.No, credit_card.durbin_regulated)
        self.assertEqual(CreditCard.Prepaid.No, credit_card.prepaid)
        self.assertEqual(CreditCard.Payroll.No, credit_card.payroll)
        self.assertEqual(CreditCard.Commercial.No, credit_card.commercial)
        self.assertEqual(CreditCard.Healthcare.No, credit_card.healthcare)
        self.assertEqual("MSB", credit_card.product_id)

    def test_card_without_card_type_indicators(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.Unknown,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEqual(CreditCard.Debit.Unknown, credit_card.debit)
        self.assertEqual(CreditCard.DurbinRegulated.Unknown, credit_card.durbin_regulated)
        self.assertEqual(CreditCard.Prepaid.Unknown, credit_card.prepaid)
        self.assertEqual(CreditCard.Payroll.Unknown, credit_card.payroll)
        self.assertEqual(CreditCard.Commercial.Unknown, credit_card.commercial)
        self.assertEqual(CreditCard.Healthcare.Unknown, credit_card.healthcare)
        self.assertEqual(CreditCard.IssuingBank.Unknown, credit_card.issuing_bank)
        self.assertEqual(CreditCard.CountryOfIssuance.Unknown, credit_card.country_of_issuance)
        self.assertEquals(CreditCard.ProductId.Unknown, credit_card.product_id)
