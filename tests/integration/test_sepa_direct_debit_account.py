from tests.test_helper import *
import time
from braintree.test.nonces import Nonces

class TestSepaDirectDebitAccount(unittest.TestCase):
    def test_find_returns_sepa_direct_debit_account(self):
        result = PaymentMethod.create({
            "customer_id": Customer.create().customer.id,
            "payment_method_nonce": Nonces.SepaDirectDebit
        })
        self.assertTrue(result.is_success)

        found_account = SepaDirectDebitAccount.find(result.payment_method.token)
        self.assertEqual(found_account.bank_reference_token, "a-fake-bank-reference-token")
        self.assertEqual(found_account.mandate_type, "RECURRENT")
        self.assertEqual(found_account.last_4, "1234")
        self.assertEqual(found_account.merchant_or_partner_customer_id, "a-fake-mp-customer-id")
        self.assertEqual(found_account.token, result.payment_method.token)
        self.assertTrue(found_account.global_id)

    def test_find_returns_subscriptions_associated_with_a_sepa_direct_debit_account(self):
        result = PaymentMethod.create({
            "customer_id": Customer.create().customer.id,
            "payment_method_nonce": Nonces.SepaDirectDebit
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

        sepa_direct_debit_account = SepaDirectDebitAccount.find(result.payment_method.token)
        self.assertTrue(subscription1.id in [s.id for s in sepa_direct_debit_account.subscriptions])
        self.assertTrue(subscription2.id in [s.id for s in sepa_direct_debit_account.subscriptions])

    def test_find_raises_on_not_found_token(self):
        self.assertRaises(NotFoundError, SepaDirectDebitAccount.find, "non-existant-token")

    def test_delete_sepa_direct_debit_account(self):
        result = PaymentMethod.create({
            "customer_id": Customer.create().customer.id,
            "payment_method_nonce": Nonces.SepaDirectDebit
        })
        self.assertTrue(result.is_success)
        sepa_direct_debit_account_token = result.payment_method.token

        delete_result = SepaDirectDebitAccount.delete(sepa_direct_debit_account_token)
        self.assertTrue(delete_result.is_success)

        self.assertRaises(NotFoundError, SepaDirectDebitAccount.find, sepa_direct_debit_account_token)

    def test_delete_raises_on_not_found(self):
        self.assertRaises(NotFoundError, SepaDirectDebitAccount.delete, "non-existant-token")
