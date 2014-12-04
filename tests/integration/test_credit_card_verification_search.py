from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers

class TestVerificationSearch(unittest.TestCase):
    def test_advanced_search_no_results(self):
        collection = CreditCardVerification.search([
            CreditCardVerificationSearch.credit_card_cardholder_name == "no such person"])
        self.assertEquals(0, collection.maximum_size)

    def test_search_on_verification_id(self):
        customer_id = "%s" % randint(1, 10000)

        result = Customer.create({
            "id": customer_id,
            "credit_card": {
                "expiration_date": "10/2018",
                "number": CreditCardNumbers.FailsSandboxVerification.Visa,
                "options": {
                    "verify_card": True
                }
            }
        })
        verification_id = result.credit_card_verification.id

        found_verifications = CreditCardVerification.search(
            CreditCardVerificationSearch.id == verification_id
        )

        self.assertEqual(1, found_verifications.maximum_size)
        self.assertEqual(verification_id, found_verifications.first.id)

    def test_all_text_fields(self):
        email = "mark.a@example.com"
        cardholder_name = "Tom %s" % randint(1, 10000)
        customer_id = "%s" % randint(1, 10000)
        expiration_date = "10/2012"
        number = CreditCardNumbers.MasterCard
        postal_code = "44444"

        customer = Customer.create({
            "id": customer_id,
            "email": email,
            "credit_card": {
                "cardholder_name": cardholder_name,
                "expiration_date": expiration_date,
                "number": number,
                "billing_address": {
                    "postal_code": postal_code
                },
                "options": {
                    "verify_card": True
                }
            }
        }).customer

        found_verifications = CreditCardVerification.search(
            CreditCardVerificationSearch.credit_card_expiration_date == expiration_date,
            CreditCardVerificationSearch.credit_card_cardholder_name == cardholder_name,
            CreditCardVerificationSearch.credit_card_number == number,
            CreditCardVerificationSearch.customer_email == email,
            CreditCardVerificationSearch.customer_id == customer_id,
            CreditCardVerificationSearch.billing_postal_code == postal_code
        )

        self.assertEqual(1, found_verifications.maximum_size)
        self.assertEqual(customer.credit_cards[0].token, found_verifications.first.credit_card["token"])

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

        verification1 = unsuccessful_result1.credit_card_verification
        verification2 = unsuccessful_result2.credit_card_verification

        search_results = CreditCardVerification.search(
                CreditCardVerificationSearch.ids.in_list([
                    verification1.id, verification2.id]),
                CreditCardVerificationSearch.credit_card_card_type.in_list([
                    verification1.credit_card["card_type"], verification2.credit_card["card_type"]]),
                CreditCardVerificationSearch.status.in_list([
                    verification1.status, verification2.status])
        )

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

