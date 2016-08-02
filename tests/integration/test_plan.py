from tests.test_helper import *

class TestPlan(unittest.TestCase):

    def test_all_returns_empty_list(self):
        Configuration.configure(
            Environment.Development,
            "test_merchant_id",
            "test_public_key",
            "test_private_key"
        )
        plans = Plan.all()
        self.assertEqual([], plans)
        Configuration.configure(
            Environment.Development,
            "integration_merchant_id",
            "integration_public_key",
            "integration_private_key"
        )

    def test_all_returns_all_the_plans(self):
        plan_token = str(random.randint(1, 1000000))
        attributes = {
            "id": plan_token,
            "billing_day_of_month": 1,
            "billing_frequency": 1,
            "currency_iso_code": "USD",
            "description": "some description",
            "name": "python test plan",
            "number_of_billing_cycles": 1,
            "price": "1.00",
        }

        Configuration.instantiate().http().post(Configuration.instantiate().base_merchant_path() + "/plans/create_plan_for_tests", {"plan": attributes})

        add_on_attributes = {
            "amount": "100.00",
            "description": "some description",
            "plan_id": plan_token,
            "kind": "add_on",
            "name": "python_add_on",
            "never_expires": False,
            "number_of_billing_cycles": 1
        }

        Configuration.instantiate().http().post(Configuration.instantiate().base_merchant_path() + "/modifications/create_modification_for_tests", {"modification": add_on_attributes})
        discount_attributes = {
            "amount": "100.00",
            "description": "some description",
            "plan_id": plan_token,
            "kind": "discount",
            "name": "python_discount",
            "never_expires": False,
            "number_of_billing_cycles": 1
        }

        Configuration.instantiate().http().post(Configuration.instantiate().base_merchant_path() + "/modifications/create_modification_for_tests", {"modification": discount_attributes})

        plans = Plan.all()

        for plan in plans:
            if plan.id == plan_token:
                actual_plan = plan

        self.assertNotEqual(None, actual_plan)

        self.assertEqual(1, attributes["billing_day_of_month"])
        self.assertEqual(1, attributes["billing_frequency"])
        self.assertEqual("USD", attributes["currency_iso_code"])
        self.assertEqual("some description", attributes["description"])
        self.assertEqual("python test plan", attributes["name"])
        self.assertEqual(1, attributes["number_of_billing_cycles"])
        self.assertEqual("1.00", attributes["price"])

        self.assertEqual(1, len(actual_plan.add_ons))
        self.assertEqual(add_on_attributes["name"], actual_plan.add_ons[0].name)

        self.assertEqual(1, len(actual_plan.discounts))
        self.assertEqual(discount_attributes["name"], actual_plan.discounts[0].name)
