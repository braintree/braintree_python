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

        self.assertNotEquals(None, add_on)

        self.assertEquals(add_on.amount, Decimal("100.00"))
        self.assertEquals(add_on.description, "some description")
        self.assertEquals(add_on.id, new_id)
        self.assertEquals(add_on.kind, "add_on")
        self.assertEquals(add_on.name, "python_add_on")
        self.assertEquals(add_on.never_expires, False)
        self.assertEquals(add_on.number_of_billing_cycles, 1)
