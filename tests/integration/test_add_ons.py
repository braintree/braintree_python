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

        Configuration.instantiate().http().post("/modifications/create_modification_for_tests", {"modification": attributes})

        add_ons = AddOn.all()

        for add_on in add_ons:
            if add_on.id == new_id:
                actual_add_on = add_on

        self.assertNotEquals(None, actual_add_on)

        self.assertEquals(attributes["amount"], "100.00")
        self.assertEquals(attributes["description"], "some description")
        self.assertEquals(attributes["id"], new_id)
        self.assertEquals(attributes["kind"], "add_on")
        self.assertEquals(attributes["name"], "python_add_on")
        self.assertEquals(attributes["never_expires"], False)
        self.assertEquals(attributes["number_of_billing_cycles"], 1)
