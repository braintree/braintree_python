from datetime import datetime
from tests.test_helper import *

from braintree.us_bank_account_verification import UsBankAccountVerification

class TestUsBankAccountVerification(unittest.TestCase):
    def test_finding_empty_id_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            UsBankAccountVerification.find(" ")

    def test_finding_none_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            UsBankAccountVerification.find(None)

    def test_attributes(self):
        attributes = {
            "id": "my_favorite_id",
            "status": "verified",
            "verification_method": "independent_check",
            "verification_determined_at": datetime(2018, 11, 11, 23, 59, 59),
            "us_bank_account": {
                "token": "abc123",
                "last_4": 9999,
            }
        }

        verification = UsBankAccountVerification({}, attributes)

        self.assertEqual(verification.id, "my_favorite_id")
        self.assertEqual(verification.status, UsBankAccountVerification.Status.Verified)
        self.assertEqual(verification.verification_determined_at, datetime(2018, 11, 11, 23, 59, 59))
        self.assertEqual(
            verification.verification_method,
            UsBankAccountVerification.VerificationMethod.IndependentCheck
        )

        self.assertEqual(verification.us_bank_account.token, "abc123")
        self.assertEqual(verification.us_bank_account.last_4, 9999)
