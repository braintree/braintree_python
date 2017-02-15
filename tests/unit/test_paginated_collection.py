from tests.test_helper import *

from braintree.paginated_collection import PaginatedCollection
from braintree.paginated_result import PaginatedResult

class TestPaginatedCollection(unittest.TestCase):
    def test_fetches_once_when_page_and_total_sizes_match(self):
        def paging_function(current_page):
            if current_page > 1:
                raise "too many pages fetched"
            else:
                return PaginatedResult(1, 1, [1])
        collection = PaginatedCollection(paging_function)

        items = [i for i in collection.items]
        self.assertEqual(1, len(items))

    def test_fetches_collections_less_than_one_page(self):
        def paging_function(current_page):
            if current_page > 1:
                raise "too many pages fetched"
            else:
                return PaginatedResult(2, 5, [1, 2])
        collection = PaginatedCollection(paging_function)

        items = [i for i in collection.items]
        self.assertEqual(2, len(items))
        self.assertEqual(1, items[0])
        self.assertEqual(2, items[1])

    def test_fetches_multiple_pages(self):
        def paging_function(current_page):
            if current_page > 2:
                raise "too many pages fetched"
            else:
                return PaginatedResult(2, 1, [current_page])
        collection = PaginatedCollection(paging_function)

        items = [i for i in collection.items]
        self.assertEqual(2, len(items))
        self.assertEqual(1, items[0])
        self.assertEqual(2, items[1])
