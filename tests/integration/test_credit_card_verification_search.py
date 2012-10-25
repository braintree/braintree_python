from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers

class TestVerificationSearch(unittest.TestCase):
    def test_advanced_search_no_results(self):
        collection = CreditCardVerification.search([
            CreditCardVerificationSearch.credit_card_cardholder_name == "no such person"])
        self.assertEquals(0, collection.maximum_size)

    def test_all_text_fields(self):
        cardholder_name = "Tom %s" % randint(1, 10000)
        expiration_date = "10/2012"
        number = CreditCardNumbers.FailsSandboxVerification.MasterCard
        unsuccessful_result = Customer.create({"credit_card": {
            "cardholder_name": cardholder_name,
            "expiration_date": expiration_date,
            "number": number,
            "options": {"verify_card": True}
        }})

        found_verifications = CreditCardVerification.search(
            CreditCardVerificationSearch.credit_card_expiration_date == expiration_date,
            CreditCardVerificationSearch.credit_card_cardholder_name == cardholder_name,
            CreditCardVerificationSearch.credit_card_number == number
        )

        self.assertEqual(1, found_verifications.maximum_size)
        created_verification = unsuccessful_result.credit_card_verification
        self.assertEqual(created_verification, found_verifications.first)

    def test_multiple_value_fields(self):
        cardholder_name = "Tom %s" % randint(1, 10000)
        number = CreditCardNumbers.FailsSandboxVerification.MasterCard
        unsuccessful_result1 = Customer.create({"credit_card": {
            "cardholder_name": cardholder_name,
            "expiration_date": "10/2013",
            "number": number,
            "options": {"verify_card": True}
        }})

        cardholder_name = "Tom %s" % randint(1, 10000)
        number = CreditCardNumbers.FailsSandboxVerification.Visa
        unsuccessful_result2 = Customer.create({"credit_card": {
            "cardholder_name": cardholder_name,
            "expiration_date": "10/2012",
            "number": number,
            "options": {"verify_card": True}
        }})

        verification_id1 = unsuccessful_result1.credit_card_verification.id
        verification_id2 = unsuccessful_result2.credit_card_verification.id

        search_results = CreditCardVerification.search(
                CreditCardVerificationSearch.ids.in_list([
                    verification_id1, verification_id2
        ]))

        self.assertEquals(2, search_results.maximum_size)

    def test_range_field(self):
        cardholder_name = "Tom %s" % randint(1, 10000)
        number = CreditCardNumbers.FailsSandboxVerification.MasterCard
        unsuccessful_result = Customer.create({"credit_card": {
            "cardholder_name": cardholder_name,
            "expiration_date": "10/2013",
            "number": number,
            "options": {"verify_card": True}
        }})

        created_verification = unsuccessful_result.credit_card_verification
        created_time = created_verification.created_at
        before_creation = created_time - timedelta(minutes=10)
        after_creation = created_time + timedelta(minutes=10)
        found_verifications = CreditCardVerification.search(
                CreditCardVerificationSearch.id == created_verification.id,
                CreditCardVerificationSearch.created_at.between(before_creation, after_creation))

        self.assertEquals(1, found_verifications.maximum_size)

        way_before_creation = created_time - timedelta(minutes=10)
        just_before_creation = created_time - timedelta(minutes=1)
        found_verifications = CreditCardVerification.search(
                CreditCardVerificationSearch.id == created_verification.id,
                CreditCardVerificationSearch.created_at.between(way_before_creation, just_before_creation))

        self.assertEquals(0, found_verifications.maximum_size)

        found_verifications = CreditCardVerification.search(
                CreditCardVerificationSearch.id == created_verification.id,
                CreditCardVerificationSearch.created_at == created_time)

        self.assertEquals(1, found_verifications.maximum_size)

