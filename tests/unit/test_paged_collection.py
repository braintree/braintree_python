from tests.test_helper import *

class TestCreditCard(unittest.TestCase):
    def test_create_paged_collection(self):
        collection_data = {
            "total_items": 2,
            "current_page_number": 3,
            "transaction": [{
                "merchant_account_id": "m_id",
                "amount": "91.23"
                }],
            "page_size": 15
        }
        collection = PagedCollection("some_query", collection_data, Transaction, "transaction")
        self.assertEquals(2, collection.total_items)
        self.assertEquals(3, collection.current_page_number)
        self.assertEquals(15, collection.page_size)

    def test_items_in_paged_collection(self):
        collection_data = {
            "total_items": 2,
            "current_page_number": 3,
            "transaction": [{
                "merchant_account_id": "m_id",
                "amount": "91.23"
                }],
            "page_size": 15
        }
        collection = PagedCollection("some_query", collection_data, Transaction, "transaction")
        self.assertEquals("m_id", collection[0].merchant_account_id)
        self.assertEquals(Decimal("91.23"), collection[0].amount)

    def test_multiple_items_in_paged_collection(self):
        collection_data = {
            "total_items": 2,
            "current_page_number": 3,
            "transaction": [{
                "merchant_account_id": "m_id",
                "amount": "91.23"
                }, {
                "merchant_account_id": "m_id2",
                "amount": "12.34"
                }],
            "page_size": 15
        }
        collection = PagedCollection("some_query", collection_data, Transaction, "transaction")
        self.assertEquals(Decimal("91.23"), collection[0].amount)
        self.assertEquals(Decimal("12.34"), collection[1].amount)
