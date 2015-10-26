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
        self.assertTrue(re.search("\A\w{4,5}\Z", credit_card.token) is not None)
        self.assertEquals("411111", credit_card.bin)
        self.assertEquals("1111", credit_card.last_4)
        self.assertEquals("05", credit_card.expiration_month)
        self.assertEquals("2014", credit_card.expiration_year)
        self.assertEquals("05/2014", credit_card.expiration_date)
        self.assertEquals("John Doe", credit_card.cardholder_name)
        self.assertNotEquals(re.search("\A\w{32}\Z", credit_card.unique_number_identifier), None)
        self.assertFalse(credit_card.venmo_sdk)
        self.assertNotEquals(re.search("png", credit_card.image_url), None)

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
        self.assertEquals("05/2014", credit_card.expiration_date)

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
        self.assertEquals(token, credit_card.token)

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
        self.assertEquals("123 Abc Way", address.street_address)
        self.assertEquals("Chicago", address.locality)
        self.assertEquals("Illinois", address.region)
        self.assertEquals("60622", address.postal_code)
        self.assertEquals("MX", address.country_code_alpha2)
        self.assertEquals("MEX", address.country_code_alpha3)
        self.assertEquals("484", address.country_code_numeric)
        self.assertEquals("Mexico", address.country_name)

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
        self.assertEquals(address.id, billing_address.id)
        self.assertEquals("123 Abc Way", billing_address.street_address)

    def test_create_without_billing_address_still_has_billing_address_method(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
        })
        self.assertTrue(result.is_success)
        self.assertEquals(None, result.credit_card.billing_address)


    def test_create_with_card_verification_returns_risk_data(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4000111111111115",
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        self.assertFalse(result.is_success)
        verification = result.credit_card_verification
        self.assertIsInstance(verification.risk_data, RiskData)
        self.assertEquals(verification.risk_data.id, None)
        self.assertEquals(verification.risk_data.decision, "Not Evaluated")

    def test_successful_create_with_card_verification_returns_risk_data(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        self.assertTrue(result.is_success)
        verification = result.credit_card.verification
        self.assertIsInstance(verification.risk_data, RiskData)
        self.assertEquals(verification.risk_data.id, None)
        self.assertEquals(verification.risk_data.decision, "Not Evaluated")

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
        self.assertEquals(CreditCardVerification.Status.ProcessorDeclined, verification.status)
        self.assertEquals("2000", verification.processor_response_code)
        self.assertEquals("Do Not Honor", verification.processor_response_text)
        self.assertEquals("I", verification.cvv_response_code)
        self.assertEquals(None, verification.avs_error_response_code)
        self.assertEquals("I", verification.avs_postal_code_response_code)
        self.assertEquals("I", verification.avs_street_address_response_code)
        self.assertEquals(TestHelper.default_merchant_account_id, verification.merchant_account_id)

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
        self.assertEquals(CreditCardVerification.Status.ProcessorDeclined, verification.status)
        self.assertEquals("2000", verification.processor_response_code)
        self.assertEquals("Do Not Honor", verification.processor_response_text)
        self.assertEquals("I", verification.cvv_response_code)
        self.assertEquals(None, verification.avs_error_response_code)
        self.assertEquals("I", verification.avs_postal_code_response_code)
        self.assertEquals("I", verification.avs_street_address_response_code)
        self.assertEquals(TestHelper.default_merchant_account_id, verification.merchant_account_id)

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
        self.assertEquals(CreditCardVerification.Status.ProcessorDeclined, verification.status)
        self.assertEquals(None, verification.gateway_rejection_reason)
        self.assertEquals(TestHelper.non_default_merchant_account_id, verification.merchant_account_id)

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
            self.assertEquals('1000', result.credit_card_verification.processor_response_code)
            self.assertEquals('Approved', result.credit_card_verification.processor_response_text)
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
            self.assertEquals(Transaction.GatewayRejectionReason.Cvv, verification.gateway_rejection_reason)
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
        self.assertEquals(ErrorCodes.CreditCard.DuplicateCardExists, result.errors.for_object("credit_card").on("number")[0].code)
        self.assertEquals("Duplicate card exists in the vault.", result.message)

    def test_create_with_invalid_invalid_options(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "invalid_date",
        })

        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.CreditCard.ExpirationDateIsInvalid, result.errors.for_object("credit_card").on("expiration_date")[0].code)
        self.assertEquals("Expiration date is invalid.", result.message)

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
        self.assertEquals(
            ErrorCodes.Address.CountryCodeAlpha2IsNotAccepted,
            result.errors.for_object("credit_card").for_object("billing_address").on("country_code_alpha2")[0].code
        )
        self.assertEquals(
            ErrorCodes.Address.CountryCodeAlpha3IsNotAccepted,
            result.errors.for_object("credit_card").for_object("billing_address").on("country_code_alpha3")[0].code
        )
        self.assertEquals(
            ErrorCodes.Address.CountryCodeNumericIsNotAccepted,
            result.errors.for_object("credit_card").for_object("billing_address").on("country_code_numeric")[0].code
        )
        self.assertEquals(
            ErrorCodes.Address.CountryNameIsNotAccepted,
            result.errors.for_object("credit_card").for_object("billing_address").on("country_name")[0].code
        )

    def test_create_with_venmo_sdk_payment_method_code(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "venmo_sdk_payment_method_code": venmo_sdk.VisaPaymentMethodCode
        })

        self.assertTrue(result.is_success)
        self.assertEquals("411111", result.credit_card.bin)
        self.assertTrue(result.credit_card.venmo_sdk)

    def test_create_with_invalid_venmo_sdk_payment_method_code(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "venmo_sdk_payment_method_code": venmo_sdk.InvalidPaymentMethodCode
        })

        self.assertFalse(result.is_success)
        self.assertEquals(result.message, "Invalid VenmoSDK payment method code")
        self.assertEquals(result.errors.for_object("credit_card") \
                .on("venmo_sdk_payment_method_code")[0].code, ErrorCodes.CreditCard.InvalidVenmoSDKPaymentMethodCode)

    def test_create_with_payment_method_nonce(self):
        config = Configuration.instantiate()
        authorization_fingerprint = json.loads(TestHelper.generate_decoded_client_token())["authorizationFingerprint"]
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
        nonce = json.loads(response)["creditCards"][0]["nonce"]
        customer = Customer.create().customer

        result = CreditCard.create({
            "customer_id": customer.id,
            "payment_method_nonce": nonce
        })

        self.assertTrue(result.is_success)
        self.assertEquals("411111", result.credit_card.bin)

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
        self.assertTrue(result.credit_card.venmo_sdk)

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
        self.assertTrue(re.search("\A\w{4,5}\Z", credit_card.token) is not None)
        self.assertEquals("510510", credit_card.bin)
        self.assertEquals("5100", credit_card.last_4)
        self.assertEquals("06", credit_card.expiration_month)
        self.assertEquals("2010", credit_card.expiration_year)
        self.assertEquals("06/2010", credit_card.expiration_date)
        self.assertEquals("Jane Jones", credit_card.cardholder_name)

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

        self.assertEquals("IL", updated_credit_card.billing_address.region)
        self.assertEquals("NG", updated_credit_card.billing_address.country_code_alpha2)
        self.assertEquals("NGA", updated_credit_card.billing_address.country_code_alpha3)
        self.assertEquals("566", updated_credit_card.billing_address.country_code_numeric)
        self.assertEquals("Nigeria", updated_credit_card.billing_address.country_name)
        self.assertEquals(None, updated_credit_card.billing_address.street_address)
        self.assertNotEquals(initial_credit_card.billing_address.id, updated_credit_card.billing_address.id)

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

        self.assertEquals("IL", updated_credit_card.billing_address.region)
        self.assertEquals("123 Nigeria Ave", updated_credit_card.billing_address.street_address)
        self.assertEquals(initial_credit_card.billing_address.id, updated_credit_card.billing_address.id)

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

        result = CreditCard.update(card2.token, {
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
        self.assertEquals(CreditCardVerification.Status.ProcessorDeclined, result.credit_card_verification.status)

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
        self.assertEquals(CreditCardVerification.Status.ProcessorDeclined, result.credit_card_verification.status)

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
        self.assertEquals("123 Abc Way", address.street_address)
        self.assertEquals("Chicago", address.locality)
        self.assertEquals("Illinois", address.region)
        self.assertEquals("60622", address.postal_code)

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
        self.assertEquals(ErrorCodes.CreditCard.ExpirationDateIsInvalid, result.errors.for_object("credit_card").on("expiration_date")[0].code)

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
        result = CreditCard.delete("notreal")

    def test_find_with_valid_token(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014"
        }).credit_card

        found_credit_card = CreditCard.find(credit_card.token)
        self.assertTrue(re.search("\A\w{4,5}\Z", credit_card.token) is not None)
        self.assertEquals("411111", credit_card.bin)
        self.assertEquals("1111", credit_card.last_4)
        self.assertEquals("05", credit_card.expiration_month)
        self.assertEquals("2014", credit_card.expiration_year)
        self.assertEquals("05/2014", credit_card.expiration_date)

    def test_find_returns_associated_subsriptions(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014"
        }).credit_card
        id = "id_" + str(random.randint(1, 1000000))
        subscription = Subscription.create({
            "id": id,
            "plan_id": "integration_trialless_plan",
            "payment_method_token": credit_card.token,
            "price": Decimal("1.00")
        }).subscription

        found_credit_card = CreditCard.find(credit_card.token)
        self.assertEquals(id, found_credit_card.subscriptions[0].id)
        self.assertEquals(Decimal("1.00"), found_credit_card.subscriptions[0].price)
        self.assertEquals(credit_card.token, found_credit_card.subscriptions[0].payment_method_token)

    def test_find_with_invalid_token(self):
        try:
            CreditCard.find("bad_token")
            self.assertTrue(False)
        except Exception as e:
            self.assertEquals("payment method with token 'bad_token' not found", str(e))

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
        self.assertEqual(status_code, 201)
        nonce = json.loads(response)["creditCards"][0]["nonce"]

        card = CreditCard.from_nonce(nonce)
        customer = Customer.find(customer.id)
        self.assertEquals(customer.credit_cards[0].token, card.token)

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
        self.assertEqual(status_code, 201)
        nonce = json.loads(response)["creditCards"][0]["nonce"]

        try:
            CreditCard.from_nonce(nonce)
            self.assertTrue(False)
        except Exception as e:
            self.assertIn("not found", str(e))

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
        self.assertEqual(status_code, 201)
        nonce = json.loads(response)["creditCards"][0]["nonce"]

        CreditCard.from_nonce(nonce)
        try:
            CreditCard.from_nonce(nonce)
            self.assertTrue(False)
        except Exception as e:
            self.assertIn("consumed", str(e))

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
        self.assertEquals("411111", credit_card.bin)
        self.assertEquals("1111", credit_card.last_4)
        self.assertEquals("05", credit_card.expiration_month)
        self.assertEquals("2012", credit_card.expiration_year)
        self.assertEquals(customer.id, credit_card.customer_id)
        self.assertEquals("MX", credit_card.billing_address.country_code_alpha2)
        self.assertEquals("MEX", credit_card.billing_address.country_code_alpha3)
        self.assertEquals("484", credit_card.billing_address.country_code_numeric)
        self.assertEquals("Mexico", credit_card.billing_address.country_name)


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
        self.assertEquals(
            ErrorCodes.CreditCard.NumberHasInvalidLength,
            result.errors.for_object("credit_card").on("number")[0].code
        )
        self.assertEquals(
            ErrorCodes.CreditCard.ExpirationDateIsInvalid,
            result.errors.for_object("credit_card").on("expiration_date")[0].code
        )

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
        self.assertEquals(new_token, credit_card.token)
        self.assertEquals("411111", credit_card.bin)
        self.assertEquals("1111", credit_card.last_4)
        self.assertEquals("05", credit_card.expiration_month)
        self.assertEquals("2014", credit_card.expiration_year)

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
        result = CreditCard.confirm_transparent_redirect(query_string)

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
        result = CreditCard.confirm_transparent_redirect(query_string)

        self.assertEquals(1, len(Customer.find(customer.id).addresses))
        updated_card = CreditCard.find(card.token)
        self.assertEquals("123 New St", updated_card.billing_address.street_address)
        self.assertEquals("Columbus", updated_card.billing_address.locality)
        self.assertEquals("Ohio", updated_card.billing_address.region)
        self.assertEquals("43215", updated_card.billing_address.postal_code)

    def test_update_from_transparent_redirect_with_error_result(self):
        old_token = str(random.randint(1, 1000000))
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
        self.assertEquals(
            ErrorCodes.CreditCard.TokenInvalid,
            result.errors.for_object("credit_card").on("token")[0].code
        )

    def test_expired_can_iterate_over_all_items(self):
        customer_id = Customer.all().first.id

        for i in range(110 - CreditCard.expired().maximum_size):
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
        self.assertEquals(collection.maximum_size, len(TestHelper.unique(credit_card_tokens)))

        self.assertEquals(set([True]), TestHelper.unique([credit_card.is_expired for credit_card in collection.items]))

    def test_expiring_between(self):
        customer_id = Customer.all().first.id

        for i in range(110 - CreditCard.expiring_between(date(2010, 1, 1), date(2010, 12, 31)).maximum_size):
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
        self.assertEquals(collection.maximum_size, len(TestHelper.unique(credit_card_tokens)))

        self.assertEquals(set(['2010']), TestHelper.unique([credit_card.expiration_year for credit_card in collection.items]))

    def test_commercial_card(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.Commercial,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEquals(CreditCard.Commercial.Yes, credit_card.commercial)

    def test_issuing_bank(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.IssuingBank,
            "expiration_date": "05/2014"
        })

        credit_card = result.credit_card

        self.assertEquals(credit_card.issuing_bank, CreditCardDefaults.IssuingBank)

    def test_country_of_issuance(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.CountryOfIssuance,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEquals(credit_card.country_of_issuance, CreditCardDefaults.CountryOfIssuance)

    def test_durbin_regulated_card(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.DurbinRegulated,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEquals(CreditCard.DurbinRegulated.Yes, credit_card.durbin_regulated)

    def test_debit_card(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.Debit,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEquals(CreditCard.Debit.Yes, credit_card.debit)

    def test_healthcare_card(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.Healthcare,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEquals(CreditCard.Healthcare.Yes, credit_card.healthcare)

    def test_payroll_card(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.Payroll,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEquals(CreditCard.Payroll.Yes, credit_card.payroll)

    def test_prepaid_card(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.Prepaid,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEquals(CreditCard.Prepaid.Yes, credit_card.prepaid)

    def test_all_negative_card_type_indicators(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.No,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEquals(CreditCard.Debit.No, credit_card.debit)
        self.assertEquals(CreditCard.DurbinRegulated.No, credit_card.durbin_regulated)
        self.assertEquals(CreditCard.Prepaid.No, credit_card.prepaid)
        self.assertEquals(CreditCard.Payroll.No, credit_card.payroll)
        self.assertEquals(CreditCard.Commercial.No, credit_card.commercial)
        self.assertEquals(CreditCard.Healthcare.No, credit_card.healthcare)

    def test_card_without_card_type_indicators(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": CreditCardNumbers.CardTypeIndicators.Unknown,
            "expiration_date": "05/2014",
            "options": {"verify_card": True}
        })

        credit_card = result.credit_card

        self.assertEquals(CreditCard.Debit.Unknown, credit_card.debit)
        self.assertEquals(CreditCard.DurbinRegulated.Unknown, credit_card.durbin_regulated)
        self.assertEquals(CreditCard.Prepaid.Unknown, credit_card.prepaid)
        self.assertEquals(CreditCard.Payroll.Unknown, credit_card.payroll)
        self.assertEquals(CreditCard.Commercial.Unknown, credit_card.commercial)
        self.assertEquals(CreditCard.Healthcare.Unknown, credit_card.healthcare)
        self.assertEquals(CreditCard.IssuingBank.Unknown, credit_card.issuing_bank)
        self.assertEquals(CreditCard.CountryOfIssuance.Unknown, credit_card.country_of_issuance)
