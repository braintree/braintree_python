from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers

class TestCreditCardVerfication(unittest.TestCase):

    def test_create_success(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "cardholder_name": "John Smith",
                "expiration_date": "05/2012"
        }})

        self.assertTrue(result.is_success)

    def test_create_failure(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.FailsSandboxVerification.MasterCard,
                "expiration_date": "05/2012"
        }})

        self.assertFalse(result.is_success)

    def test_create_returns_validation_errors(self):
        result = CreditCardVerification.create({
            "credit_card": {
                "number": CreditCardNumbers.FailsSandboxVerification.MasterCard,
                "expiration_date": "05/2012"
            },
            "options": {"amount": "-10.00"}
        })

        self.assertFalse(result.is_success)

        amount_errors = result.errors.for_object("verification").for_object("options").on("amount")
        self.assertEqual(1, len(amount_errors))
        self.assertEqual(ErrorCodes.Verification.Options.AmountCannotBeNegative, amount_errors[0].code)

    def test_find_with_verification_id(self):
        customer = Customer.create({
            "credit_card": {
                "number": CreditCardNumbers.FailsSandboxVerification.MasterCard,
                "expiration_date": "05/2012",
                "cardholder_name": "Tom Smith",
                "options": {"verify_card": True}
        }})

        created_verification = customer.credit_card_verification
        found_verification = CreditCardVerification.find(created_verification.id)
        self.assertEqual(created_verification, found_verification)

    def test_verification_not_found(self):
        self.assertRaises(NotFoundError, CreditCardVerification.find,
          "invalid-id")

    def test_card_type_indicators(self):
        cardholder_name = "Tom %s" % random.randint(1, 10000)
        Customer.create({"credit_card": {
            "cardholder_name": cardholder_name,
            "expiration_date": "10/2012",
            "number": CreditCardNumbers.CardTypeIndicators.Unknown,
            "options": {"verify_card": True}
        }})
        found_verifications = CreditCardVerification.search(
            CreditCardVerificationSearch.credit_card_cardholder_name == cardholder_name
        )

        self.assertEqual(CreditCard.Prepaid.Unknown, found_verifications.first.credit_card['prepaid'])
        self.assertEqual(CreditCard.Debit.Unknown, found_verifications.first.credit_card['debit'])
        self.assertEqual(CreditCard.Commercial.Unknown, found_verifications.first.credit_card['commercial'])
        self.assertEqual(CreditCard.Healthcare.Unknown, found_verifications.first.credit_card['healthcare'])
        self.assertEqual(CreditCard.Payroll.Unknown, found_verifications.first.credit_card['payroll'])
        self.assertEqual(CreditCard.DurbinRegulated.Unknown, found_verifications.first.credit_card['durbin_regulated'])
        self.assertEqual(CreditCard.IssuingBank.Unknown, found_verifications.first.credit_card['issuing_bank'])
        self.assertEqual(CreditCard.CountryOfIssuance.Unknown, found_verifications.first.credit_card['country_of_issuance'])
        self.assertEqual(CreditCard.ProductId.Unknown, found_verifications.first.credit_card['product_id'])
