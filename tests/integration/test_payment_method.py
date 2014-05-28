from tests.test_helper import *
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
        token = ClientToken.generate({"customer_id": customer_id, "sepa_mandate_type": SEPABankAccount.MandateType.Business})
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
            "billingAddress": {"region": "Hesse"}
        })

        self.assertNotEquals(nonce, None)
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": nonce
        })

        self.assertTrue(result.is_success)
        found_bank_account = PaymentMethod.find(result.payment_method.token)

        self.assertNotEqual(found_bank_account, None)
        self.assertEquals(found_bank_account.bic, "DEUTDEFF")
        self.assertEquals(found_bank_account.__class__, SEPABankAccount)

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
