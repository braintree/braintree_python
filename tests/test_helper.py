import unittest
from braintree.configuration import Configuration
from braintree.environment import Environment

Configuration.environment = Environment.DEVELOPMENT
Configuration.merchant_id = "integration_merchant_id"
Configuration.public_key = "integration_public_key"
Configuration.private_key = "integration_private_key"
