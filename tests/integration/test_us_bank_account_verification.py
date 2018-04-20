from tests.test_helper import *

from braintree.us_bank_account_verification import UsBankAccountVerification
from braintree.us_bank_account_verification_search import UsBankAccountVerificationSearch

class TestUsBankAccountVerification(unittest.TestCase):
    def test_find_by_id(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce(),
            "options": {
                "verification_merchant_account_id": TestHelper.us_bank_merchant_account_id,
                "us_bank_account_verification_method": UsBankAccountVerification.VerificationMethod.IndependentCheck
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual(len(result.payment_method.verifications), 1)

        created_verification = result.payment_method.verifications[0]

        found_verification = UsBankAccountVerification.find(created_verification.id)

        self.assertEqual(created_verification, found_verification)

    def test_search_by_verification_method(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce(),
            "options": {
                "verification_merchant_account_id": TestHelper.us_bank_merchant_account_id,
                "us_bank_account_verification_method": UsBankAccountVerification.VerificationMethod.IndependentCheck
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual(len(result.payment_method.verifications), 1)

        created_verification = result.payment_method.verifications[0]

        found_verifications = UsBankAccountVerification.search(
            UsBankAccountVerificationSearch.verification_method.in_list(
                [UsBankAccountVerification.VerificationMethod.IndependentCheck]
            ),
            UsBankAccountVerificationSearch.customer_id == customer_id,
        )

        self.assertEqual(1, found_verifications.maximum_size)
        self.assertEqual(created_verification, found_verifications.first)

    def test_search_by_status(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce(),
            "options": {
                "verification_merchant_account_id": TestHelper.us_bank_merchant_account_id,
                "us_bank_account_verification_method": UsBankAccountVerification.VerificationMethod.IndependentCheck
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual(len(result.payment_method.verifications), 1)

        created_verification = result.payment_method.verifications[0]

        found_verifications = UsBankAccountVerification.search(
            UsBankAccountVerificationSearch.status.in_list([UsBankAccountVerification.Status.Verified]),
            UsBankAccountVerificationSearch.customer_id == customer_id,
        )

        self.assertEqual(1, found_verifications.maximum_size)
        self.assertEqual(created_verification, found_verifications.first)

    def test_search_by_account_number(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce(account_number="1000000000"),
            "options": {
                "verification_merchant_account_id": TestHelper.us_bank_merchant_account_id,
                "us_bank_account_verification_method": UsBankAccountVerification.VerificationMethod.IndependentCheck
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual(len(result.payment_method.verifications), 1)

        created_verification = result.payment_method.verifications[0]

        found_verifications = UsBankAccountVerification.search(
            UsBankAccountVerificationSearch.account_number.ends_with("0000"),
            UsBankAccountVerificationSearch.customer_id == customer_id,
        )

        self.assertEqual(1, found_verifications.maximum_size)
        self.assertEqual(created_verification, found_verifications.first)

class TestUsBankAccountVerificationCompliant(unittest.TestCase):
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

    def test_successfully_confirm_settled_micro_transfer_amounts(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce(account_number="1000000000"),
            "options": {
                "verification_merchant_account_id": TestHelper.another_us_bank_merchant_account_id,
                "us_bank_account_verification_method": UsBankAccountVerification.VerificationMethod.MicroTransfers
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual(len(result.payment_method.verifications), 1)

        verification = result.payment_method.verifications[0]

        self.assertEqual(verification.status, UsBankAccountVerification.Status.Pending)
        self.assertEqual(verification.verification_method, UsBankAccountVerification.VerificationMethod.MicroTransfers)

        result = UsBankAccountVerification.confirm_micro_transfer_amounts(verification.id, [17, 29])

        self.assertTrue(result.is_success)

        self.assertEqual(result.us_bank_account_verification.status, UsBankAccountVerification.Status.Verified)

        us_bank_account = UsBankAccount.find(result.us_bank_account_verification.us_bank_account.token)

        self.assertTrue(us_bank_account.verified)

    def test_successfully_confirm_unsettled_micro_transfer_amounts(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce(account_number="1000000001"),
            "options": {
                "verification_merchant_account_id": TestHelper.another_us_bank_merchant_account_id,
                "us_bank_account_verification_method": UsBankAccountVerification.VerificationMethod.MicroTransfers
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual(len(result.payment_method.verifications), 1)

        verification = result.payment_method.verifications[0]

        self.assertEqual(verification.status, UsBankAccountVerification.Status.Pending)
        self.assertEqual(verification.verification_method, UsBankAccountVerification.VerificationMethod.MicroTransfers)

        result = UsBankAccountVerification.confirm_micro_transfer_amounts(verification.id, [17, 29])

        self.assertTrue(result.is_success)

        self.assertEqual(result.us_bank_account_verification.status, UsBankAccountVerification.Status.Pending)

        us_bank_account = UsBankAccount.find(result.us_bank_account_verification.us_bank_account.token)

        self.assertFalse(us_bank_account.verified)

    def test_attempt_confirm_micro_transfer_amounts(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce(account_number="1000000000"),
            "options": {
                "verification_merchant_account_id": TestHelper.another_us_bank_merchant_account_id,
                "us_bank_account_verification_method": UsBankAccountVerification.VerificationMethod.MicroTransfers
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual(len(result.payment_method.verifications), 1)

        verification = result.payment_method.verifications[0]

        self.assertEqual(verification.status, UsBankAccountVerification.Status.Pending)
        self.assertEqual(verification.verification_method, UsBankAccountVerification.VerificationMethod.MicroTransfers)

        result = UsBankAccountVerification.confirm_micro_transfer_amounts(verification.id, [1, 1])

        self.assertFalse(result.is_success)

        error_code = result.errors.for_object("us_bank_account_verification").on("base")[0].code
        self.assertEqual(ErrorCodes.UsBankAccountVerification.AmountsDoNotMatch, error_code)

    def test_gateway_reject_confirm_micro_transfer_amounts(self):
        customer_id = Customer.create().customer.id
        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce(account_number="1000000000"),
            "options": {
                "verification_merchant_account_id": TestHelper.another_us_bank_merchant_account_id,
                "us_bank_account_verification_method": UsBankAccountVerification.VerificationMethod.MicroTransfers
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual(len(result.payment_method.verifications), 1)

        verification = result.payment_method.verifications[0]

        self.assertEqual(verification.status, UsBankAccountVerification.Status.Pending)
        self.assertEqual(verification.verification_method, UsBankAccountVerification.VerificationMethod.MicroTransfers)

        for i in range(4):
            result = UsBankAccountVerification.confirm_micro_transfer_amounts(verification.id, [1, 1])
            self.assertFalse(result.is_success)
            error_code = result.errors.for_object("us_bank_account_verification").on("base")[0].code
            self.assertEqual(ErrorCodes.UsBankAccountVerification.AmountsDoNotMatch, error_code)

        result = UsBankAccountVerification.confirm_micro_transfer_amounts(verification.id, [1, 1])
        self.assertFalse(result.is_success)
        error_code = result.errors.for_object("us_bank_account_verification").on("base")[0].code
        self.assertEqual(ErrorCodes.UsBankAccountVerification.TooManyConfirmationAttempts, error_code)
