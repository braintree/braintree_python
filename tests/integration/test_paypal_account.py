from tests.test_helper import *
import time
from braintree.test.nonces import Nonces

class TestPayPalAccount(unittest.TestCase):
    def test_find_returns_paypal_account(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.PayPalBillingAgreement
        })
        self.assertTrue(result.is_success)

        found_account = PayPalAccount.find(result.payment_method.token)
        self.assertNotEqual(None, found_account)
        self.assertEqual(found_account.__class__, PayPalAccount)
        self.assertEqual(found_account.token, result.payment_method.token)
        self.assertNotEqual(None, found_account.image_url)
        self.assertNotEqual(None, found_account.created_at)
        self.assertNotEqual(None, found_account.updated_at)
        self.assertIsNone(found_account.funding_source_description) 
        self.assertFalse(hasattr(found_account, "edit_paypal_vault_id"))
        self.assertIsNone(found_account.revoked_at)

    def test_find_raises_on_not_found_token(self):
        self.assertRaises(NotFoundError, PayPalAccount.find, "non-existant-token")

    def test_find_will_not_return_credit_card(self):
        credit_card = CreditCard.create({
            "customer_id": Customer.create().customer.id,
            "number": "4111111111111111",
            "expiration_date": "12/2099"
        }).credit_card

        self.assertRaises(NotFoundError, PayPalAccount.find, credit_card.token)

    def test_find_returns_subscriptions_associated_with_a_paypal_account(self):
        customer_id = Customer.create().customer.id
        payment_method_token = "paypal-account-" + str(int(time.time()))

        nonce = TestHelper.nonce_for_paypal_account({
            "consent_code": "consent-code",
            "token": payment_method_token
        })
        result = PaymentMethod.create({
            "payment_method_nonce": nonce,
            "customer_id": customer_id
        })
        self.assertTrue(result.is_success)

        token = result.payment_method.token

        subscription1 = Subscription.create({
            "payment_method_token": token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription

        subscription2 = Subscription.create({
            "payment_method_token": token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription

        paypal_account = PayPalAccount.find(result.payment_method.token)
        self.assertTrue(subscription1.id in [s.id for s in paypal_account.subscriptions])
        self.assertTrue(subscription2.id in [s.id for s in paypal_account.subscriptions])

    def test_find_retuns_billing_agreement_id_with_a_paypal_account(self):
        customer_id = Customer.create().customer.id

        result = PaymentMethod.create({
            "payment_method_nonce": Nonces.PayPalBillingAgreement,
            "customer_id": customer_id
        })
        self.assertTrue(result.is_success)

        paypal_account = PayPalAccount.find(result.payment_method.token)
        self.assertNotEqual(None, paypal_account.billing_agreement_id)

    def test_delete_customer_with_path_traversal(self):
        try:
            customer = Customer.create({"first_name":"Waldo"}).customer
            PayPalAccount.delete("../../{}".format(customer.id))
        except NotFoundError:
            pass

        found_customer = Customer.find(customer.id)
        self.assertNotEqual(None, found_customer)
        self.assertEqual("Waldo", found_customer.first_name)


    def test_delete_deletes_paypal_account(self):
        result = PaymentMethod.create({
            "customer_id": Customer.create().customer.id,
            "payment_method_nonce": Nonces.PayPalBillingAgreement
        })
        self.assertTrue(result.is_success)
        paypal_account_token = result.payment_method.token

        delete_result = PayPalAccount.delete(paypal_account_token)
        self.assertTrue(delete_result.is_success)

        self.assertRaises(NotFoundError, PayPalAccount.find, paypal_account_token)

    def test_delete_raises_on_not_found(self):
        self.assertRaises(NotFoundError, PayPalAccount.delete, "non-existant-token")

    def test_delete_delete_wont_delete_credit_card(self):
        credit_card = CreditCard.create({
            "customer_id": Customer.create().customer.id,
            "number": "4111111111111111",
            "expiration_date": "12/2099"
        }).credit_card

        self.assertRaises(NotFoundError, PayPalAccount.delete, credit_card.token)

    def test_update_can_update_token_and_default(self):
        customer_id = Customer.create().customer.id

        CreditCard.create({
            "customer_id": customer_id,
            "number": "4111111111111111",
            "expiration_date": "12/2099"
        })

        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.PayPalFuturePayment
        })
        self.assertTrue(result.is_success)

        old_token = result.payment_method.token
        new_token = "new-token-%s" % int(round(time.time() * 1000))
        result = PayPalAccount.update(old_token, {
            "token": new_token,
            "options": {"make_default": True}
        })

        self.assertTrue(result.is_success)
        updated_account = PayPalAccount.find(new_token)
        self.assertEqual(updated_account.default, True)

    def test_update_returns_validation_errors(self):
        payment_method_token = "payment-token-%s" % int(round(time.time() * 1000))
        customer_id = Customer.create().customer.id
        CreditCard.create({
            "token": payment_method_token,
            "customer_id": customer_id,
            "number": "4111111111111111",
            "expiration_date": "12/2099"
        })

        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.PayPalFuturePayment
        })
        self.assertTrue(result.is_success)

        old_token = result.payment_method.token
        result = PayPalAccount.update(old_token, {
            "token": payment_method_token,
        })
        self.assertFalse(result.is_success)

        token_errors = result.errors.for_object("paypal_account").on("token")
        self.assertEqual(1, len(token_errors))
        self.assertEqual(ErrorCodes.PayPalAccount.TokenIsInUse, token_errors[0].code)

        result = PayPalAccount.update(old_token, {
            "token": payment_method_token,
        })
        self.assertFalse(result.is_success)

        token_errors = result.errors.for_object("paypal_account").on("token")
        self.assertEqual(1, len(token_errors))
        self.assertEqual(ErrorCodes.PayPalAccount.TokenIsInUse, token_errors[0].code)
