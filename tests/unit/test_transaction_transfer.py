from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers
from braintree.payment_facilitator import PaymentFacilitator
from braintree.sub_merchant import SubMerchant
from braintree.meta_checkout_card import MetaCheckoutCard
from braintree.meta_checkout_token import MetaCheckoutToken
from datetime import datetime
from datetime import date
from braintree.authorization_adjustment import AuthorizationAdjustment
from unittest.mock import MagicMock


class TestTransactionTransferType(unittest.TestCase):
    def test_aft_transfer_type(self):
        attributes = {
                "amount": TransactionAmounts.Authorize,
                "transfer": {
                    "type": "wallet_transfer",
                    },
                }

        transaction = Transaction(None, attributes)
        self.assertEqual(transaction.transfer.type, 'wallet_transfer')
