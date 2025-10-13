import unittest
from braintree import BraintreeGateway, Environment, BankAccountInstantVerificationGateway


class TestBraintreeGatewayBankAccount(unittest.TestCase):

    def test_bank_account_instant_verification_returns_gateway_instance(self):
        gateway = BraintreeGateway(
            environment=Environment.Development,
            merchant_id="merchant_id",
            public_key="public_key",
            private_key="private_key"
        )

        bank_account_instant_verification_gateway = gateway.bank_account_instant_verification

        self.assertIsNotNone(bank_account_instant_verification_gateway)
        self.assertIsInstance(bank_account_instant_verification_gateway, BankAccountInstantVerificationGateway)