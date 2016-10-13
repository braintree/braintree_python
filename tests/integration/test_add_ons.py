from tests.test_helper import *

class TestAddOn(unittest.TestCase):
    def test_all_returns_all_add_ons(self):
        new_id = str(random.randint(1, 1000000))
        attributes = {
            "amount": "100.00",
            "description": "some description",
            "id": new_id,
            "kind": "add_on",
            "name": "python_add_on",
            "never_expires": False,
            "number_of_billing_cycles": 1
        }

        Configuration.instantiate().http().post(Configuration.instantiate().base_merchant_path() + "/modifications/create_modification_for_tests", {"modification": attributes})

        add_ons = AddOn.all()

        for add_on in add_ons:
            if add_on.id == new_id:
                break
        else:
            add_on = None

        self.assertNotEqual(None, add_on)

        self.assertEqual(Decimal("100.00"), add_on.amount)
        self.assertEqual("some description", add_on.description)
        self.assertEqual(new_id, add_on.id)
        self.assertEqual("add_on", add_on.kind)
        self.assertEqual("python_add_on", add_on.name)
        self.assertEqual(False, add_on.never_expires)
        self.assertEqual(add_on.number_of_billing_cycles, 1)
