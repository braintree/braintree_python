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
        collection = PagedCollection("some_query", collection_data, Transaction)
        self.assertEquals(2, collection.total_items)
        self.assertEquals(3, collection.current_page_number)
        self.assertEquals(15, collection.page_size)

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
        collection = PagedCollection("some_query", collection_data, Transaction)
        self.assertEquals(Decimal("91.23"), collection[0].amount)
        self.assertEquals(Decimal("12.34"), collection[1].amount)

    def test_only_one_item_in_paged_colleciton(self):
        collection_data = {
            "total_items": 1,
            "current_page_number": 1,
            "transaction": {
                "merchant_account_id": "m_id",
                "amount": "91.23"
                },
            "page_size": 15
        }
        collection = PagedCollection("some_query", collection_data, Transaction)
        self.assertEquals(Decimal("91.23"), collection[0].amount)

    def test_no_items_in_paged_colleciton(self):
        collection_data = {
            "total_items": 0,
            "current_page_number": 1,
            "page_size": 15
        }
        collection = PagedCollection("some_query", collection_data, Transaction)
        self.assertEquals(0, collection.total_items)
        self.assertEquals(0, collection.current_page_size)
        self.assertEquals(1, collection.current_page_number)
        self.assertTrue(collection.is_last_page)

    def test_total_pages_for_evenly_divisible_total_items(self):
        collection_data = {
            "total_items": 30,
            "page_size": 10,
            "current_page_number": 3,
            "transaction": []
        }
        collection = PagedCollection("some_query", collection_data, Transaction)

        self.assertEquals(3, collection.total_pages)

    def test_total_pages_for_non_evenly_divisible_total_items(self):
        collection_data = {
            "total_items": 32,
            "page_size": 10,
            "current_page_number": 3,
            "transaction": []
        }
        collection = PagedCollection("some_query", collection_data, Transaction)

        self.assertEquals(4, collection.total_pages)

    def test_current_page_size_for_full_page(self):
        collection_data = {
            "total_items": 32,
            "page_size": 10,
            "current_page_number": 2,
            "transaction": []
        }
        collection = PagedCollection("some_query", collection_data, Transaction)

        self.assertEquals(10, collection.current_page_size)

    def test_is_last_page_on_last_page(self):
        collection_data = {
            "total_items": 32,
            "page_size": 10,
            "current_page_number": 4,
            "transaction": []
        }
        collection = PagedCollection("some_query", collection_data, Transaction)

        self.assertTrue(collection.is_last_page)

    def test_is_last_page_not_on_last_page(self):
        collection_data = {
            "total_items": 32,
            "page_size": 10,
            "current_page_number": 2,
            "transaction": []
        }
        collection = PagedCollection("some_query", collection_data, Transaction)

        self.assertFalse(collection.is_last_page)
