from tests.test_helper import *
from braintree.test.nonces import Nonces
from braintree.credentials_parser import CredentialsParser

class TestCredentialsParser(unittest.TestCase):
    def test_parses_client_credentials(self):
        parser = CredentialsParser(
            client_id = "client_id$development$integration_client_id",
            client_secret = "client_secret$development$integration_client_secret"
        )
        parser.parse_client_credentials()

        self.assertEqual(parser.client_id, "client_id$development$integration_client_id")
        self.assertEqual(parser.client_secret, "client_secret$development$integration_client_secret")
        self.assertEqual(parser.environment, braintree.Environment.Development)

    def test_error_on_inconsistent_environment(self):
        with self.assertRaises(ConfigurationError) as error:
            parser = CredentialsParser(
                client_id = "client_id$qa$integration_client_id",
                client_secret = "client_secret$development$integration_client_secret"
            )
            parser.parse_client_credentials()

        config_error = error.exception
        self.assertIn("Mismatched credential environments", str(config_error))

    def test_error_on_missing_client_id(self):
        with self.assertRaises(ConfigurationError) as error:
            parser = CredentialsParser(
                client_id = None,
                client_secret = "client_secret$development$integration_client_secret"
            )
            parser.parse_client_credentials()

        config_error = error.exception
        self.assertIn("Missing client_id", str(config_error))

    def test_error_on_missing_client_secret(self):
        with self.assertRaises(ConfigurationError) as error:
            parser = CredentialsParser(
                client_id = "client_id$development$integration_client_id",
                client_secret = None
            )
            parser.parse_client_credentials()

        config_error = error.exception
        self.assertIn("Missing client_secret", str(config_error))

    def test_error_on_invalid_client_id(self):
        with self.assertRaises(ConfigurationError) as error:
            parser = CredentialsParser(
                client_id = "client_secret$development$integration_client_id",
                client_secret = "client_secret$development$integration_client_secret"
            )
            parser.parse_client_credentials()

        config_error = error.exception
        self.assertIn("Value passed for client_id is not a client_id", str(config_error))

    def test_error_on_invalid_client_secret(self):
        with self.assertRaises(ConfigurationError) as error:
            parser = CredentialsParser(
                client_id = "client_id$development$integration_client_id",
                client_secret = "client_id$development$integration_client_secret"
            )
            parser.parse_client_credentials()

        config_error = error.exception
        self.assertIn("Value passed for client_secret is not a client_secret", str(config_error))

    def test_parses_access_token(self):
        parser = CredentialsParser(
            access_token = "access_token$development$integration_merchant_id$fb27c79dd"
        )
        parser.parse_access_token()

        self.assertEqual(parser.access_token, "access_token$development$integration_merchant_id$fb27c79dd")
        self.assertEqual(parser.merchant_id, "integration_merchant_id")
        self.assertEqual(parser.environment, braintree.Environment.Development)
