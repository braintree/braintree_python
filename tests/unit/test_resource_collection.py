from tests.test_helper import *

class TestResourceCollection(unittest.TestCase):
    def test_approximate_size(self):
        collection_data = {
            "total_items": 2,
            "current_page_number": 1,
            "transaction": [{"amount": "91.23"}, {"amount": "123"}],
            "page_size": 15
        }
        collection = ResourceCollection("some_query", collection_data, Transaction)
        self.assertEquals(2, collection.approximate_size)

    def test_multiple_items_in_collection(self):
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
        collection = ResourceCollection("some_query", collection_data, Transaction)
        self.assertEquals([Decimal("91.23"), Decimal("12.34")], [Decimal(t.amount) for t in collection.items])

    def test_only_one_item_in_colleciton(self):
        collection_data = {
            "total_items": 1,
            "current_page_number": 1,
            "transaction": {
                "merchant_account_id": "m_id",
                "amount": "91.23"
                },
            "page_size": 15
        }
        collection = ResourceCollection("some_query", collection_data, Transaction)
        self.assertEquals(Decimal("91.23"), collection.first.amount)

    def test_no_items_in_colleciton(self):
        collection_data = {
            "total_items": 0,
            "current_page_number": 1,
            "page_size": 15
        }
        collection = ResourceCollection("some_query", collection_data, Transaction)
        self.assertEquals(0, collection.approximate_size)

    def test_first_returns_None_if_no_items(self):
        collection_data = {
            "total_items": 0,
            "current_page_number": 1,
            "transaction": [],
            "page_size": 15
        }
        collection = ResourceCollection("some_query", collection_data, Transaction)
        self.assertEquals(None, collection.first)

    def test_first_returns_first_item(self):
        collection_data = {
            "total_items": 2,
            "current_page_number": 1,
            "transaction": [
                { "amount": "1.23"},
                { "amount": "2.34"}
            ],
            "page_size": 15
        }
        collection = ResourceCollection("some_query", collection_data, Transaction)
        self.assertEquals(Decimal("1.23"), collection.first.amount)
