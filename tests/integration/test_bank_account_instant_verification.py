from tests.test_helper import *
from braintree.configuration import Configuration
from braintree.us_bank_account_verification import UsBankAccountVerification
import requests
import json

class TestBankAccountInstantVerification(unittest.TestCase):

    def setUp(self):
        self.gateway = BraintreeGateway(
            Configuration(
                environment=Environment.Development,
                merchant_id="integration2_merchant_id",
                public_key="integration2_public_key",
                private_key="integration2_private_key"
            )
        )

        self.us_bank_gateway = BraintreeGateway(
            Configuration(
                environment=Environment.Development,
                merchant_id="integration_merchant_id",
                public_key="integration_public_key",
                private_key="integration_private_key"
            )
        )

    def assert_has_attributes(self, obj, expected_attributes):
        """Helper method to assert that an object has the expected attributes"""
        for key, expected_value in expected_attributes.items():
            actual_value = getattr(obj, key)

            if isinstance(expected_value, dict) and hasattr(actual_value, '__dict__'):
                # Recursively check nested objects
                self.assert_has_attributes(actual_value, expected_value)
            elif callable(expected_value):
                # Handle type checks and regex patterns
                self.assertTrue(expected_value(actual_value), "Expected {} to match predicate, got {}".format(key, actual_value))
            elif expected_value is not None:
                self.assertEqual(expected_value, actual_value, "Expected {} to be {}, got {}".format(key, expected_value, actual_value))
            else:
                self.assertIsNotNone(actual_value, "Expected {} to not be None".format(key))

    def generate_us_bank_account_nonce_via_open_banking(self):
        config = Configuration(
            environment=Environment.Development,
            merchant_id="integration_merchant_id",
            public_key="integration_public_key",
            private_key="integration_private_key"
        )
        
        # Use the new Open Banking REST API endpoint to tokenize without ACH mandate
        request_body = {
            "account_details": {
                "account_number": "567891234",
                "account_type": "CHECKING",
                "classification": "PERSONAL",
                "tokenized_account": True,
                "last_4": "1234"
            },
            "institution_details": {
                "bank_id": {
                    "bank_code": "021000021",
                    "country_code": "US"
                }
            },
            "account_holders": [
                {
                    "ownership": "PRIMARY",
                    "full_name": {
                        "name": "Dan Schulman"
                    },
                    "name": {
                        "given_name": "Dan",
                        "surname": "Schulman",
                        "full_name": "Dan Schulman"
                    }
                }
            ]
        }
        
        graphql_base_url = config.graphql_base_url()
        atmosphere_base_url = graphql_base_url.replace('/graphql', '')
        url = atmosphere_base_url + '/v1/open-finance/tokenize-bank-account-details'
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Braintree-Version': '2019-01-01',
            'User-Agent': 'Braintree Python Library {}'.format(braintree.version.Version),
            'X-ApiVersion': Configuration.api_version()
        }
        
        response = requests.post(
            url,
            json=request_body,
            headers=headers,
            auth=(config.public_key, config.private_key),
            timeout=config.timeout
        )

        if response.status_code != 200:
            raise Exception('HTTP error {}: {}'.format(response.status_code, response.text))

        response_data = response.json()
        if 'tenant_token' not in response_data:
            raise Exception('Open Banking tokenization failed: {}'.format(response_data))
        
        return response_data['tenant_token']

    def test_create_jwt_creates_a_jwt_with_valid_request(self):
        request = BankAccountInstantVerificationJwtRequest()
        request.business_name("15Ladders")
        request.return_url("https://example.com/success")
        request.cancel_url("https://example.com/cancel")

        result = self.gateway.bank_account_instant_verification.create_jwt(request)

        self.assertTrue(result.is_success, "Expected success but got errors: {}".format(getattr(result, 'errors', 'none')))
        self.assertIsNotNone(result.bank_account_instant_verification_jwt)
        self.assertIsNotNone(result.bank_account_instant_verification_jwt.jwt)
        self.assertNotEqual("", result.bank_account_instant_verification_jwt.jwt)

        self.assertTrue(result.bank_account_instant_verification_jwt.jwt.startswith("eyJ"))


    def test_create_jwt_fails_with_invalid_business_name(self):
        request = BankAccountInstantVerificationJwtRequest()
        request.business_name("")  # Empty business name should cause validation error
        request.return_url("https://example.com/return")
        request.cancel_url("https://example.com/cancel")

        result = self.gateway.bank_account_instant_verification.create_jwt(request)

        self.assertFalse(result.is_success, 'Expected failure but got success')
        self.assertIsNotNone(result.errors, 'Expected errors but got none')

    def test_create_jwt_fails_with_invalid_urls(self):
        request = BankAccountInstantVerificationJwtRequest()
        request.business_name("15Ladders")
        request.return_url("not-a-valid-url")
        request.cancel_url("also-not-valid")

        result = self.us_bank_gateway.bank_account_instant_verification.create_jwt(request)

        self.assertFalse(result.is_success, 'Expected failure but got success')
        self.assertIsNotNone(result.errors, 'Expected errors but got none')

    def test_charge_us_bank_creates_transaction_directly_with_nonce_and_provides_ach_mandate_at_transaction_time_instant_verification(self):
        nonce = self.generate_us_bank_account_nonce_via_open_banking()

        mandate_accepted_at = datetime.now() - timedelta(minutes=5)

        # Create transaction directly with nonce and provide ACH mandate at transaction time (instant verification)
        transaction_request = {
            "amount": Decimal("12.34"),
            "payment_method_nonce": nonce,
            "merchant_account_id": TestHelper.us_bank_merchant_account_id,
            "us_bank_account": {
                "ach_mandate_text": "I authorize this transaction and future debits",
                "ach_mandate_accepted_at": mandate_accepted_at
            },
            "options": {
                "submit_for_settlement": True
            }
        }

        transaction_result = self.us_bank_gateway.transaction.sale(transaction_request)

        self.assertTrue(transaction_result.is_success, "Expected transaction success but got failure with validation errors")
        transaction = transaction_result.transaction

        expected_transaction = {
            "id": lambda x: isinstance(x, str) and len(x) > 0,
            "amount": Decimal("12.34"),
            "us_bank_account": {
                "ach_mandate": {
                    "text": "I authorize this transaction and future debits",
                    "accepted_at": lambda x: isinstance(x, datetime)
                },
                "account_holder_name": "Dan Schulman",
                "last_4": "1234",
                "routing_number": "021000021",
                "account_type": "checking"
            }
        }

        self.assert_has_attributes(transaction, expected_transaction)

    def test_open_finance_flow_tokenizes_bank_account_via_open_finance_api_vaults_with_and_charges(self):
        nonce = self.generate_us_bank_account_nonce_via_open_banking()

        customer_result = self.us_bank_gateway.customer.create({})
        self.assertTrue(customer_result.is_success)
        customer = customer_result.customer

        mandate_accepted_at = datetime.now() - timedelta(minutes=5)

        payment_method_request = {
            "customer_id": customer.id,
            "payment_method_nonce": nonce,
            "us_bank_account": {
                "ach_mandate_text": "I authorize this transaction and future debits",
                "ach_mandate_accepted_at": mandate_accepted_at
            },
            "options": {
                "verification_merchant_account_id": TestHelper.us_bank_merchant_account_id,
                "us_bank_account_verification_method": UsBankAccountVerification.VerificationMethod.InstantVerificationAccountValidation
            }
        }

        payment_method_result = self.us_bank_gateway.payment_method.create(payment_method_request)
        self.assertTrue(payment_method_result.is_success, "Expected payment method creation success but got failure with validation errors")

        us_bank_account = payment_method_result.payment_method

        expected_us_bank_account = {
            "verifications": lambda x: (
                x is not None and
                len(x) == 1 and
                x[0].verification_method == UsBankAccountVerification.VerificationMethod.InstantVerificationAccountValidation and
                x[0].status == "verified"
            ),
            "ach_mandate": {
                "text": "I authorize this transaction and future debits",
                "accepted_at": lambda x: isinstance(x, datetime)
            }
        }

        self.assert_has_attributes(us_bank_account, expected_us_bank_account)

        verification = us_bank_account.verifications[0]
        self.assertEqual(UsBankAccountVerification.VerificationMethod.InstantVerificationAccountValidation, verification.verification_method)

        transaction_request = {
            "amount": Decimal("12.34"),
            "payment_method_token": us_bank_account.token,
            "merchant_account_id": TestHelper.us_bank_merchant_account_id,
            "options": {
                "submit_for_settlement": True
            }
        }

        transaction_result = self.us_bank_gateway.transaction.sale(transaction_request)
        self.assertTrue(transaction_result.is_success, "Expected transaction success but got failure")
        transaction = transaction_result.transaction

        expected_transaction = {
            "id": lambda x: isinstance(x, str) and len(x) > 0,
            "amount": Decimal("12.34"),
            "us_bank_account": {
                "token": us_bank_account.token,
                "ach_mandate": {
                    "text": "I authorize this transaction and future debits",
                    "accepted_at": lambda x: isinstance(x, datetime)
                },
                "last_4": "1234",
                "routing_number": "021000021",
                "account_type": "checking"
            }
        }

        self.assert_has_attributes(transaction, expected_transaction)

