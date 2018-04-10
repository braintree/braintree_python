from tests.test_helper import *
from braintree.us_bank_account_verification import UsBankAccountVerification

class PaymentMethodWithUsBankAccountTest(unittest.TestCase):
    def test_create_with_nonce(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce(),
            "options": {
                "verification_merchant_account_id": TestHelper.us_bank_merchant_account_id
            }
        })

        self.assertTrue(result.is_success)
        us_bank_account = result.payment_method
        self.assertIsInstance(us_bank_account, UsBankAccount)
        self.assertEqual(us_bank_account.routing_number, "021000021")
        self.assertEqual(us_bank_account.last_4, "1234")
        self.assertEqual(us_bank_account.account_type, "checking")
        self.assertEqual(us_bank_account.account_holder_name, "Dan Schulman")
        self.assertTrue(re.match(r".*CHASE.*", us_bank_account.bank_name))
        self.assertEqual(us_bank_account.default, True)
        self.assertEqual(us_bank_account.ach_mandate.text, "cl mandate text")
        self.assertIsInstance(us_bank_account.ach_mandate.accepted_at, datetime)
        self.assertEqual(us_bank_account.verified, True)

        self.assertEqual(len(us_bank_account.verifications), 1)

        verification = us_bank_account.verifications[0]

        self.assertEqual(verification.status, "verified")
        self.assertEqual(verification.verification_method, UsBankAccountVerification.VerificationMethod.IndependentCheck)

    def test_create_with_verification(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce("021000021", "1000000000"),
            "options": {
                "verification_merchant_account_id": TestHelper.us_bank_merchant_account_id,
                "us_bank_account_verification_method": UsBankAccountVerification.VerificationMethod.NetworkCheck,
            }
        })

        self.assertTrue(result.is_success)
        us_bank_account = result.payment_method
        self.assertIsInstance(us_bank_account, UsBankAccount)
        self.assertEqual(us_bank_account.routing_number, "021000021")
        self.assertEqual(us_bank_account.last_4, "0000")
        self.assertEqual(us_bank_account.account_type, "checking")
        self.assertEqual(us_bank_account.account_holder_name, "Dan Schulman")
        self.assertTrue(re.match(r".*CHASE.*", us_bank_account.bank_name))
        self.assertEqual(us_bank_account.default, True)
        self.assertEqual(us_bank_account.ach_mandate.text, "cl mandate text")
        self.assertIsInstance(us_bank_account.ach_mandate.accepted_at, datetime)
        self.assertEqual(us_bank_account.verified, True)

        self.assertEqual(len(us_bank_account.verifications), 1)

        verification = us_bank_account.verifications[0]

        self.assertEqual(verification.status, UsBankAccountVerification.Status.Verified)
        self.assertEqual(verification.verification_method, UsBankAccountVerification.VerificationMethod.NetworkCheck)

    def test_create_fails_with_invalid_us_bank_account_nonce(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_invalid_us_bank_account_nonce(),
            "options": {
                "verification_merchant_account_id": TestHelper.us_bank_merchant_account_id
            }
        })

        self.assertFalse(result.is_success)
        error_code = result.errors.for_object("payment_method").on("payment_method_nonce")[0].code
        self.assertEqual(ErrorCodes.PaymentMethod.PaymentMethodNonceUnknown, error_code)

    def test_update_payment_method_with_verification(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce("021000021", "1000000000"),
            "options": {
                "verification_merchant_account_id": TestHelper.us_bank_merchant_account_id,
            }
        })

        self.assertTrue(result.is_success)
        us_bank_account = result.payment_method

        self.assertEqual(len(us_bank_account.verifications), 1)

        verification = us_bank_account.verifications[0]

        self.assertEqual(verification.status, UsBankAccountVerification.Status.Verified)
        self.assertEqual(verification.verification_method, UsBankAccountVerification.VerificationMethod.IndependentCheck)

        result = PaymentMethod.update(us_bank_account.token, {
            "options": {
                "verification_merchant_account_id": TestHelper.us_bank_merchant_account_id,
                "us_bank_account_verification_method": UsBankAccountVerification.VerificationMethod.NetworkCheck,
            }
        })

        self.assertTrue(result.is_success)
        us_bank_account = result.payment_method

        self.assertEqual(len(us_bank_account.verifications), 2)

class PaymentMethodWithUsBankAccountCompliantMerchantTest(unittest.TestCase):
    def setUp(self):
        braintree.Configuration.configure(
            braintree.Environment.Development,
            "integration2_merchant_id",
            "integration2_public_key",
            "integration2_private_key"
        )

    def tearDown(self):
        braintree.Configuration.configure(
            braintree.Environment.Development,
            "integration_merchant_id",
            "integration_public_key",
            "integration_private_key"
        )

    def test_create_with_nonce(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce(),
            "options": {
                "verification_merchant_account_id": TestHelper.another_us_bank_merchant_account_id
            }
        })

        self.assertTrue(result.is_success)
        us_bank_account = result.payment_method
        self.assertIsInstance(us_bank_account, UsBankAccount)
        self.assertEqual(us_bank_account.routing_number, "021000021")
        self.assertEqual(us_bank_account.last_4, "1234")
        self.assertEqual(us_bank_account.account_type, "checking")
        self.assertEqual(us_bank_account.account_holder_name, "Dan Schulman")
        self.assertTrue(re.match(r".*CHASE.*", us_bank_account.bank_name))
        self.assertEqual(us_bank_account.default, True)
        self.assertEqual(us_bank_account.ach_mandate.text, "cl mandate text")
        self.assertIsInstance(us_bank_account.ach_mandate.accepted_at, datetime)
        self.assertEqual(us_bank_account.verified, False)

        self.assertEqual(len(us_bank_account.verifications), 0)

    def test_create_with_verification(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce("021000021", "1000000000"),
            "options": {
                "verification_merchant_account_id": TestHelper.another_us_bank_merchant_account_id,
                "us_bank_account_verification_method": UsBankAccountVerification.VerificationMethod.NetworkCheck
            }
        })

        self.assertTrue(result.is_success)
        us_bank_account = result.payment_method
        self.assertIsInstance(us_bank_account, UsBankAccount)
        self.assertEqual(us_bank_account.routing_number, "021000021")
        self.assertEqual(us_bank_account.last_4, "0000")
        self.assertEqual(us_bank_account.account_type, "checking")
        self.assertEqual(us_bank_account.account_holder_name, "Dan Schulman")
        self.assertTrue(re.match(r".*CHASE.*", us_bank_account.bank_name))
        self.assertEqual(us_bank_account.default, True)
        self.assertEqual(us_bank_account.ach_mandate.text, "cl mandate text")
        self.assertIsInstance(us_bank_account.ach_mandate.accepted_at, datetime)
        self.assertEqual(us_bank_account.verified, True)

        self.assertEqual(len(us_bank_account.verifications), 1)

        verification = us_bank_account.verifications[0]

        self.assertEqual(verification.status, UsBankAccountVerification.Status.Verified)

    def test_create_fails_with_invalid_us_bank_account_nonce(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_invalid_us_bank_account_nonce(),
            "options": {
                "verification_merchant_account_id": TestHelper.another_us_bank_merchant_account_id,
                "us_bank_account_verification_method": UsBankAccountVerification.VerificationMethod.NetworkCheck,
            }
        })

        self.assertFalse(result.is_success)
        error_code = result.errors.for_object("payment_method").on("payment_method_nonce")[0].code
        self.assertEqual(ErrorCodes.PaymentMethod.PaymentMethodNonceUnknown, error_code)

    def test_update_payment_method_with_verification(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce("021000021", "1000000000"),
            "options": {
                "verification_merchant_account_id": TestHelper.another_us_bank_merchant_account_id,
                "us_bank_account_verification_method": UsBankAccountVerification.VerificationMethod.IndependentCheck
            }
        })

        self.assertTrue(result.is_success)
        us_bank_account = result.payment_method

        self.assertEqual(len(us_bank_account.verifications), 1)

        verification = us_bank_account.verifications[0]

        self.assertEqual(verification.status, UsBankAccountVerification.Status.Verified)
        self.assertEqual(verification.verification_method, UsBankAccountVerification.VerificationMethod.IndependentCheck)

        result = PaymentMethod.update(us_bank_account.token, {
            "options": {
                "verification_merchant_account_id": TestHelper.another_us_bank_merchant_account_id,
                "us_bank_account_verification_method": UsBankAccountVerification.VerificationMethod.NetworkCheck,
            }
        })

        self.assertTrue(result.is_success)
        us_bank_account = result.payment_method

        self.assertEqual(len(us_bank_account.verifications), 2)
