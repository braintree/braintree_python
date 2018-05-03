from tests.test_helper import *
from datetime import date
from braintree.us_bank_account import UsBankAccount
from braintree.us_bank_account_verification import UsBankAccountVerification

class TestUsBankAccount(unittest.TestCase):
    def test_constructor(self):
        attributes = {
            "last_four": "1234",
            "routing_number": "55555",
            "account_type": "fake-account",
            "account_holder_name": "John Doe",
            "token": "7777-7777",
            "image_url": "some.png",
            "bank_name": "Chase",
            "ach_mandate": None,
        }

        us_bank_account = UsBankAccount({}, attributes)
        self.assertEqual(us_bank_account.last_four, "1234")
        self.assertEqual(us_bank_account.routing_number, "55555")
        self.assertEqual(us_bank_account.account_type, "fake-account")
        self.assertEqual(us_bank_account.account_holder_name, "John Doe")
        self.assertEqual(us_bank_account.token, "7777-7777")
        self.assertEqual(us_bank_account.image_url, "some.png")
        self.assertEqual(us_bank_account.bank_name, "Chase")
        self.assertEqual(us_bank_account.ach_mandate, None)

        attributes["ach_mandate"] = {"text":"Some mandate", "accepted_at": date(2013, 4, 10)}
        us_bank_account_mandated = UsBankAccount({}, attributes)
        self.assertEqual(us_bank_account_mandated.ach_mandate.text, "Some mandate")
        self.assertEqual(us_bank_account_mandated.ach_mandate.accepted_at, date(2013, 4, 10))

    def test_converts_verifications_to_objects(self):
        attributes = {
            "verifications": [
                {
                    "status": "verified",
                    "verification_method": "network_check",
                },
            ],
        }

        us_bank_account = UsBankAccount({}, attributes)
        self.assertEqual(len(us_bank_account.verifications), 1)

        verification = us_bank_account.verifications[0]

        self.assertEqual(verification.status, UsBankAccountVerification.Status.Verified)
        self.assertEqual(verification.verification_method, UsBankAccountVerification.VerificationMethod.NetworkCheck)
