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

        Configuration.instantiate().http().post(Configuration.instantiate().base_merchant_path() + "/modifications/create_modification_for_tests", {"modification": attributes})

        discounts = Discount.all()

        for discount in discounts:
            if discount.id == new_id:
                break
        else:
            discount = None

        self.assertNotEqual(None, discount)

        self.assertEqual(Decimal("100.00"), discount.amount)
        self.assertEqual("some description", discount.description)
        self.assertEqual(new_id, discount.id)
        self.assertEqual("discount", discount.kind)
        self.assertEqual("python_discount", discount.name)
        self.assertEqual(False, discount.never_expires)
        self.assertEqual(1, discount.number_of_billing_cycles)
