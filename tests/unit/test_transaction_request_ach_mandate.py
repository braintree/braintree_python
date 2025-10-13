import unittest
from datetime import datetime
from braintree.transaction_us_bank_account_request import TransactionUsBankAccountRequest


class TestTransactionRequestAchMandate(unittest.TestCase):

    def test_to_param_dict_includes_ach_mandate(self):
        parent = object()  # Mock parent
        request = TransactionUsBankAccountRequest(parent)
        request.ach_mandate_text("I authorize this ACH debit transaction")

        params = request.to_param_dict()
        
        self.assertIn("ach_mandate_text", params)
        self.assertEqual("I authorize this ACH debit transaction", params["ach_mandate_text"])

    def test_to_param_dict_includes_ach_mandate_accepted_at(self):
        parent = object()  # Mock parent
        request = TransactionUsBankAccountRequest(parent)
        accepted_at = datetime(2024, 1, 15, 14, 30, 0)
        request.ach_mandate_accepted_at(accepted_at)

        params = request.to_param_dict()
        
        self.assertIn("ach_mandate_accepted_at", params)
        self.assertEqual(accepted_at.isoformat(), params["ach_mandate_accepted_at"])

    def test_to_param_dict_includes_both_ach_mandate_fields(self):
        parent = object()  # Mock parent
        request = TransactionUsBankAccountRequest(parent)
        accepted_at = datetime(2024, 1, 15, 14, 30, 0)
        request.ach_mandate_text("I authorize this ACH debit transaction")
        request.ach_mandate_accepted_at(accepted_at)

        params = request.to_param_dict()
        
        self.assertIn("ach_mandate_text", params)
        self.assertEqual("I authorize this ACH debit transaction", params["ach_mandate_text"])
        self.assertIn("ach_mandate_accepted_at", params)
        self.assertEqual(accepted_at.isoformat(), params["ach_mandate_accepted_at"])

    def test_fluent_interface_returns_correct_instance(self):
        parent = object()  # Mock parent
        request = TransactionUsBankAccountRequest(parent)
        accepted_at = datetime.now()

        result = (request
                 .ach_mandate_text("Test mandate")
                 .ach_mandate_accepted_at(accepted_at))

        self.assertIs(request, result)
        
    def test_done_returns_parent(self):
        parent = object()  # Mock parent
        request = TransactionUsBankAccountRequest(parent)
        
        result = request.done()
        
        self.assertIs(parent, result)

    def test_to_param_dict_omits_none_ach_mandate_fields(self):
        parent = object()  # Mock parent
        request = TransactionUsBankAccountRequest(parent)
        request.ach_mandate_text(None)
        request.ach_mandate_accepted_at(None)

        params = request.to_param_dict()
        
        self.assertNotIn("ach_mandate_text", params)
        self.assertNotIn("ach_mandate_accepted_at", params)

    def test_ach_mandate_handles_special_characters(self):
        parent = object()  # Mock parent
        request = TransactionUsBankAccountRequest(parent)
        request.ach_mandate_text('I authorize this ACH debit & transaction <with> special "characters"')

        params = request.to_param_dict()
        
        # Python doesn't need XML escaping in the param dict - that's handled at serialization
        self.assertEqual('I authorize this ACH debit & transaction <with> special "characters"', 
                        params["ach_mandate_text"])