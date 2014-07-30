import time
from random import randint
from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers
from braintree.test.nonces import Nonces

class TestPaymentMethod(unittest.TestCase):
    def test_create_with_paypal_future_payments_nonce(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.PayPalFuturePayment
        })

        self.assertTrue(result.is_success)
        created_account = result.payment_method
        self.assertEquals(created_account.__class__, PayPalAccount)
        self.assertEquals(created_account.email, "jane.doe@example.com")
        self.assertNotEquals(created_account.image_url, None)

        found_account = PaymentMethod.find(result.payment_method.token)
        self.assertNotEqual(None, found_account)
        self.assertEquals(found_account.token, created_account.token)

    def test_create_returns_validation_failures(self):
        http = ClientApiHttp.create()
        status_code, nonce = http.get_paypal_nonce({
            "options": {"validate": False}
        })
        self.assertEquals(status_code, 202)
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
        self.assertEquals(token, result.payment_method.token)

    def test_create_with_paypal_one_time_nonce_fails(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.PayPalOneTimePayment
        })

        self.assertFalse(result.is_success)
        error_code = result.errors.for_object("paypal_account").on("base")[0].code
        self.assertEquals(error_code, ErrorCodes.PayPalAccount.CannotVaultOneTimeUsePayPalAccount)

    def test_create_with_credit_card_nonce(self):
        http = ClientApiHttp.create()
        status_code, nonce = http.get_credit_card_nonce({
            "number": "4111111111111111",
            "expirationMonth": "12",
            "expirationYear": "2020",
            "options": {"validate": False}
        })
        self.assertEquals(status_code, 202)

        customer_id = Customer.create().customer.id

        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": nonce
        })

        self.assertTrue(result.is_success)
        created_credit_card = result.payment_method
        self.assertEquals(created_credit_card.__class__, CreditCard)
        self.assertEquals(created_credit_card.bin, "411111")

        found_credit_card = PaymentMethod.find(result.payment_method.token)
        self.assertNotEqual(None, found_credit_card)
        self.assertEquals(found_credit_card.token, created_credit_card.token)

    def test_create_with_sepa_bank_account_nonce(self):
        config = Configuration.instantiate()
        customer_id = Customer.create().customer.id
        token = TestHelper.generate_decoded_client_token({"customer_id": customer_id, "sepa_mandate_type": SEPABankAccount.MandateType.Business})
        authorization_fingerprint = json.loads(token)["authorizationFingerprint"]
        client_api =  ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing"
        })
        nonce = client_api.get_sepa_bank_account_nonce({
            "locale": "de-DE",
            "bic": "DEUTDEFF",
            "iban": "DE89370400440532013000",
            "accountHolderName": "Baron Von Holder",
            "billingAddress": {"region": "Hesse", "country_name": "Germany"}
        })

        self.assertNotEquals(nonce, None)
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": nonce
        })

        self.assertTrue(result.is_success)
        self.assertNotEqual(result.payment_method.image_url, None)
        found_bank_account = PaymentMethod.find(result.payment_method.token)

        self.assertNotEqual(found_bank_account, None)
        self.assertEquals(found_bank_account.bic, "DEUTDEFF")
        self.assertEquals(found_bank_account.__class__, SEPABankAccount)

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
        self.assertTrue(type(payment_method_result.payment_method) is CreditCard)
        token = payment_method_result.payment_method.token

        found_credit_card = CreditCard.find(token)
        self.assertFalse(found_credit_card == None)
        self.assertTrue(found_credit_card.billing_address.first_name == "Bobby")
        self.assertTrue(found_credit_card.billing_address.last_name == "Tables")

    def test_create_for_paypal_ignores_passed_billing_address_id(self):
        nonce = Nonces.nonce_for_paypal_account({
            "consent_code": "consent-code"
        })
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "payment_method_nonce": nonce,
            "customer_id": customer_id,
            "billing_address_id": "address_id"
        })

        self.assertTrue(result.is_success)
        self.assertTrue(type(result.payment_method) is PayPalAccount)
        self.assertFalse(result.payment_method.image_url == None)
        token = result.payment_method.token

        found_paypal_account = PayPalAccount.find(token)
        self.assertFalse(found_paypal_account == None)

    def test_find_returns_a_paypal_account(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.PayPalFuturePayment
        })
        self.assertTrue(result.is_success)

        found_account = PaymentMethod.find(result.payment_method.token)
        self.assertNotEqual(None, found_account)
        self.assertEquals(found_account.__class__, PayPalAccount)
        self.assertEquals(found_account.email, "jane.doe@example.com")

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
        credit_card = result.credit_card

        found_credit_card = PaymentMethod.find(result.credit_card.token)
        self.assertNotEqual(None, found_credit_card)
        self.assertEquals(found_credit_card.__class__, CreditCard)
        self.assertEquals(found_credit_card.bin, "411111")

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

        delete_result = PaymentMethod.delete(result.payment_method.token)
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
                "region": "IL"
            }
        })
        self.assertTrue(update_result.is_success)
        updated_credit_card = update_result.payment_method
        self.assertTrue(updated_credit_card.billing_address.region == "IL")
        self.assertTrue(updated_credit_card.billing_address.street_address == None)
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
        self.assertTrue(update_result.credit_card_verification.gateway_rejection_reason == None)

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
            "options": { "verify_card": "false" },
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
        self.assertTrue(update_result.errors.for_object("credit_card").on("number")[0].message == "Credit card number must be 12-19 digits.")

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

        self.assertTrue(card1.default == True)
        self.assertTrue(card2.default == False)

        update_result = PaymentMethod.update(card2.token, {
            "options": { "make_default": True }
        })

        self.assertTrue(CreditCard.find(card1.token).default == False)
        self.assertTrue(CreditCard.find(card2.token).default == True)

    def test_update_updates_a_paypal_accounts_token(self):
        customer_id = Customer.create().customer.id
        original_token = "paypal-account-" + str(int(time.time()))
        nonce = Nonces.nonce_for_paypal_account({
            "consent_code": "consent-code",
            "token": original_token
        })
        original_result = PaymentMethod.create({
             "payment_method_nonce": nonce,
             "customer_id": customer_id
        })

        updated_token = "UPDATED_TOKEN-" + str(randint(0,100000000))
        updated_result = PaymentMethod.update(
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

        nonce = Nonces.nonce_for_paypal_account({
            "consent_code": "consent-code"
        })
        original_token = PaymentMethod.create({
             "payment_method_nonce": nonce,
             "customer_id": customer_id
        }).payment_method.token

        updated_result = PaymentMethod.update(
            original_token,
            {"options": {"make_default": "true"}}
        )

        updated_paypal_account = PayPalAccount.find(original_token)
        self.assertTrue(updated_paypal_account.default == True)

    def test_update_updates_a_paypal_accounts_token(self):
        customer_id = Customer.create().customer.id
        first_token = "paypal-account-" + str(randint(0,100000000))
        second_token = "paypal-account-" + str(randint(0,100000000))

        first_nonce = Nonces.nonce_for_paypal_account({
            "consent_code": "consent-code",
            "token": first_token
        })
        first_result = PaymentMethod.create({
             "payment_method_nonce": first_nonce,
             "customer_id": customer_id
        })

        second_nonce = Nonces.nonce_for_paypal_account({
            "consent_code": "consent-code",
            "token": second_token
        })
        second_result = PaymentMethod.create({
             "payment_method_nonce": second_nonce,
             "customer_id": customer_id
        })

        updated_result = PaymentMethod.update(
            first_token,
            {"token": second_token}
        )

        self.assertTrue(updated_result.is_success == False)
        self.assertTrue(updated_result.errors.deep_errors[0].code == "92906")

class CreditCardForwardingTest(unittest.TestCase):
    def setUp(self):
        braintree.Configuration.configure(
            braintree.Environment.Development,
            "forward_payment_method_merchant_id",
            "forward_payment_method_public_key",
            "forward_payment_method_private_key"
        )

    def tearDown(self):
        braintree.Configuration.configure(
            braintree.Environment.Development,
            "integration_merchant_id",
            "integration_public_key",
            "integration_private_key"
        )

    def test_forward(self):
        customer = Customer.create().customer
        credit_card_result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2025"
        })
        self.assertTrue(credit_card_result.is_success)
        source_merchant_card = credit_card_result.credit_card

        forward_result = CreditCard.forward(
            source_merchant_card.token,
            "integration_merchant_id"
        )
        self.assertTrue(forward_result.is_success)

        braintree.Configuration.configure(
            braintree.Environment.Development,
            "integration_merchant_id",
            "integration_public_key",
            "integration_private_key"
        )
        customer = Customer.create().customer
        credit_card_result = CreditCard.create({
            "customer_id": customer.id,
            "payment_method_nonce": forward_result.nonce
        })
        self.assertTrue(credit_card_result.is_success)
        receiving_merchant_card = credit_card_result.credit_card
        self.assertEqual(source_merchant_card.bin, receiving_merchant_card.bin)
        self.assertEqual(source_merchant_card.last_4, receiving_merchant_card.last_4)
        self.assertEqual(source_merchant_card.expiration_month, receiving_merchant_card.expiration_month)
        self.assertEqual(source_merchant_card.expiration_year, receiving_merchant_card.expiration_year)

    def test_forward_invalid_token_raises_exception(self):
        self.assertRaises(NotFoundError, CreditCard.forward, "invalid", "integration_merchant_id")

    def test_forward_invalid_receiving_merchant_raises_exception(self):
        customer = Customer.create().customer
        credit_card_result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2025"
        })
        self.assertTrue(credit_card_result.is_success)
        source_merchant_card = credit_card_result.credit_card

        self.assertRaises(NotFoundError, CreditCard.forward, source_merchant_card.token, "invalid_merchant_id")
