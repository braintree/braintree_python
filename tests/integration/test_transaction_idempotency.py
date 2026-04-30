import random
from tests.test_helper import *

class TestTransactionIdempotency(unittest.TestCase):

    def test_sale_with_api_request_key_returns_original_transaction_on_duplicate_request(self):
        api_request_key = "idempotency-key-%d" % random.randint(0, 1000000)

        transaction_params = {
            "amount": TransactionAmounts.Authorize,
            "api_request_key": api_request_key,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2035"
            }
        }

        result1 = Transaction.sale(transaction_params)
        self.assertTrue(result1.is_success)
        transaction1 = result1.transaction
        self.assertIsNotNone(transaction1.id)

        result2 = Transaction.sale(transaction_params)
        self.assertTrue(result2.is_success)
        transaction2 = result2.transaction

        self.assertEqual(transaction1.status, transaction2.status)
        self.assertEqual(transaction1.id, transaction2.id)

    def test_sale_with_api_request_key_fails_when_different_request_used_with_same_key(self):
        api_request_key = "idempotency-key-%d" % random.randint(0, 1000000)

        transaction_params1 = {
            "amount": TransactionAmounts.Authorize,
            "api_request_key": api_request_key,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2035"
            }
        }

        result1 = Transaction.sale(transaction_params1)
        self.assertTrue(result1.is_success)

        transaction_params2 = {
            "amount": "200.00",
            "api_request_key": api_request_key,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2035"
            }
        }

        result2 = Transaction.sale(transaction_params2)

        self.assertFalse(result2.is_success)
        self.assertIsNotNone(result2.errors)
        errors = result2.errors.deep_errors
        self.assertTrue(len(errors) > 0)
        self.assertEqual(ErrorCodes.Transaction.ApiRequestKeyCanBeReusedOnlyWithTheSameRequest, errors[0].code)

    def test_submit_for_partial_settlement_with_api_request_key_returns_original_on_duplicate_request(self):
        api_request_key = "partial-settlement-idempotency-key-%d" % random.randint(0, 1000000)

        sale_request = {
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2035"
            }
        }

        sale_result = Transaction.sale(sale_request)
        self.assertTrue(sale_result.is_success)
        transaction_id = sale_result.transaction.id

        partial_amount = "50.00"
        partial_settlement_request = {
            "api_request_key": api_request_key
        }

        partial_settlement_result1 = Transaction.submit_for_partial_settlement(
            transaction_id,
            partial_amount,
            partial_settlement_request
        )
        self.assertTrue(partial_settlement_result1.is_success)
        partial_settlement_transaction1 = partial_settlement_result1.transaction
        self.assertEqual(Decimal(partial_amount), partial_settlement_transaction1.amount)
        self.assertIsNotNone(partial_settlement_transaction1.id)

        partial_settlement_result2 = Transaction.submit_for_partial_settlement(
            transaction_id,
            partial_amount,
            partial_settlement_request
        )
        self.assertTrue(partial_settlement_result2.is_success)
        partial_settlement_transaction2 = partial_settlement_result2.transaction

        self.assertEqual(partial_settlement_transaction1.id, partial_settlement_transaction2.id)
        self.assertEqual(partial_settlement_transaction1.amount, partial_settlement_transaction2.amount)

    def test_submit_for_settlement_with_api_request_key_returns_original_on_duplicate_request(self):
        api_request_key = "settlement-idempotency-key-%d" % random.randint(0, 1000000)

        sale_request = {
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2035"
            }
        }

        sale_result = Transaction.sale(sale_request)
        self.assertTrue(sale_result.is_success)
        transaction_id = sale_result.transaction.id
        original_amount = sale_result.transaction.amount

        settlement_request = {
            "api_request_key": api_request_key
        }

        settlement_result1 = Transaction.submit_for_settlement(
            transaction_id,
            None,
            settlement_request
        )
        self.assertTrue(settlement_result1.is_success)
        settlement_transaction1 = settlement_result1.transaction
        self.assertEqual(original_amount, settlement_transaction1.amount)
        self.assertIsNotNone(settlement_transaction1.id)

        settlement_result2 = Transaction.submit_for_settlement(
            transaction_id,
            None,
            settlement_request
        )
        self.assertTrue(settlement_result2.is_success)
        settlement_transaction2 = settlement_result2.transaction

        self.assertEqual(settlement_transaction1.id, settlement_transaction2.id)
        self.assertEqual(settlement_transaction1.amount, settlement_transaction2.amount)

    def test_void_with_api_request_key_returns_original_void_on_duplicate_request(self):
        api_request_key = "void-idempotency-key-%d" % random.randint(0, 1000000)

        sale_request = {
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2035"
            }
        }

        sale_result = Transaction.sale(sale_request)
        self.assertTrue(sale_result.is_success)
        transaction_id = sale_result.transaction.id

        void_request = {
            "api_request_key": api_request_key
        }

        void_result1 = Transaction.void(transaction_id, void_request)
        self.assertTrue(void_result1.is_success)
        voided_transaction1 = void_result1.transaction
        self.assertEqual(Transaction.Status.Voided, voided_transaction1.status)

        void_result2 = Transaction.void(transaction_id, void_request)
        self.assertTrue(void_result2.is_success)
        voided_transaction2 = void_result2.transaction

        self.assertEqual(voided_transaction1.id, voided_transaction2.id)
        self.assertEqual(voided_transaction1.status, voided_transaction2.status)
        self.assertEqual(Transaction.Status.Voided, voided_transaction2.status)

    def test_refund_with_api_request_key_returns_original_refund_on_duplicate_request(self):
        api_request_key = "refund-idempotency-key-%d" % random.randint(0, 1000000)

        sale_request = {
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2035"
            },
            "options": {
                "submit_for_settlement": True
            }
        }

        sale_result = Transaction.sale(sale_request)
        self.assertTrue(sale_result.is_success)
        transaction_id = sale_result.transaction.id

        config = Configuration.instantiate()
        gateway = BraintreeGateway(config)
        settled_transaction = TestingGateway(gateway).settle_transaction(transaction_id)
        self.assertEqual(Transaction.Status.Settled, settled_transaction.transaction.status)

        refund_request = {
            "api_request_key": api_request_key
        }

        refund_result1 = Transaction.refund(transaction_id, refund_request)
        self.assertTrue(refund_result1.is_success)
        refund_transaction1 = refund_result1.transaction
        self.assertEqual(Transaction.Type.Credit, refund_transaction1.type)
        self.assertIsNotNone(refund_transaction1.id)

        refund_result2 = Transaction.refund(transaction_id, refund_request)
        self.assertTrue(refund_result2.is_success)
        refund_transaction2 = refund_result2.transaction

        self.assertEqual(refund_transaction1.id, refund_transaction2.id)
        self.assertEqual(refund_transaction1.type, refund_transaction2.type)

    def test_same_sales_with_different_api_request_key(self):
        api_request_key1 = "idempotency-key-%d" % random.randint(0, 1000000)

        transaction_params1 = {
            "amount": TransactionAmounts.Authorize,
            "api_request_key": api_request_key1,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2035"
            }
        }

        result1 = Transaction.sale(transaction_params1)
        self.assertTrue(result1.is_success)
        transaction1 = result1.transaction
        self.assertIsNotNone(transaction1.id)

        api_request_key2 = "idempotency-key-%d" % random.randint(0, 1000000)
        transaction_params2 = {
            "amount": TransactionAmounts.Authorize,
            "api_request_key": api_request_key2,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2035"
            }
        }
        result2 = Transaction.sale(transaction_params2)
        self.assertTrue(result2.is_success)
        transaction2 = result2.transaction

        self.assertNotEqual(transaction1.id, transaction2.id)

    def test_sale_with_api_request_key_fails_when_api_request_key_is_too_big(self):
        transaction_params1 = {
            "amount": TransactionAmounts.Authorize,
            "api_request_key": "x" * 255,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2035"
            }
        }

        result1 = Transaction.sale(transaction_params1)
        self.assertTrue(result1.is_success)

        transaction_params2 = {
            "amount": "200.00",
            "api_request_key": "x" * 256,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2035"
            }
        }

        result2 = Transaction.sale(transaction_params2)

        self.assertFalse(result2.is_success)
        self.assertIsNotNone(result2.errors)
        errors = result2.errors.deep_errors
        self.assertTrue(len(errors) > 0)
        self.assertEqual(ErrorCodes.Transaction.ApiRequestKeyTooLong, errors[0].code)

    def test_credit_with_api_request_key_returns_original_on_duplicate_request(self):
        api_request_key = "credit-idempotency-key-%d" % random.randint(0, 1000000)

        transaction_params = {
            "amount": TransactionAmounts.Authorize,
            "api_request_key": api_request_key,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2035"
            }
        }

        credit_result1 = Transaction.credit(transaction_params)
        self.assertTrue(credit_result1.is_success)
        credit_transaction1 = credit_result1.transaction
        self.assertEqual(Transaction.Type.Credit, credit_transaction1.type)
        self.assertIsNotNone(credit_transaction1.id)

        credit_result2 = Transaction.credit(transaction_params)
        self.assertTrue(credit_result2.is_success)
        credit_transaction2 = credit_result2.transaction

        self.assertEqual(credit_transaction1.id, credit_transaction2.id)
        self.assertEqual(credit_transaction1.type, credit_transaction2.type)
