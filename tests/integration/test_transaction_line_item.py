from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers

class TestTransactionLineItem(unittest.TestCase):

    def test_transaction_line_item_find_all_returns_line_items(self):
        transaction = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "total_amount": "45.15",
                "upc_code": "123456789",
                "upc_type": "UPC-A",
                "image_url": "https://google.com/image.png",
            }]
        }).transaction

        line_items = TransactionLineItem.find_all(transaction.id)
        self.assertEqual(1, len(line_items))
        lineItem = line_items[0]
        self.assertEqual("1.0232", lineItem.quantity)
        self.assertEqual("Name #1", lineItem.name)
        self.assertEqual(TransactionLineItem.Kind.Debit, lineItem.kind)
        self.assertEqual("45.1232", lineItem.unit_amount)
        self.assertEqual("45.15", lineItem.total_amount)
        self.assertEqual("123456789", lineItem.upc_code)
        self.assertEqual("UPC-A", lineItem.upc_type)
        self.assertEqual("https://google.com/image.png",lineItem.image_url)

