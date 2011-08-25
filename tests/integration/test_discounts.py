from tests.test_helper import *

class TestDiscounts(unittest.TestCase):

    def test_all_returns_all_discounts(self):
        new_id = str(random.randint(1, 1000000))
        attributes = {
            "amount": "100.00",
            "description": "some description",
            "id": new_id,
            "kind": "discount",
            "name": "python_discount",
            "never_expires": False,
            "number_of_billing_cycles": 1
        }

        Configuration.instantiate().http().post("/modifications/create_modification_for_tests", {"modification": attributes})

        discounts = Discount.all()

        for discount in discounts:
            if discount.id == new_id:
                actual_discount = discount

        self.assertNotEquals(None, actual_discount)

        self.assertEquals(attributes["amount"], "100.00")
        self.assertEquals(attributes["description"], "some description")
        self.assertEquals(attributes["id"], new_id)
        self.assertEquals(attributes["kind"], "discount")
        self.assertEquals(attributes["name"], "python_discount")
        self.assertEquals(attributes["never_expires"], False)
        self.assertEquals(attributes["number_of_billing_cycles"], 1)
