from tests.test_helper import *

class TestResourceCollection(unittest.TestCase):
    collection_data = {
        "search_results": {
            "page_size": 2,
            "ids": ["0", "1", "2", "3", "4"]
        }
    }

    class TestResource:
        items = ["a", "b", "c", "d", "e"]

        @staticmethod
        def fetch(query, ids):
            return [TestResourceCollection.TestResource.items[int(id)] for id in ids]

    def test_iterating_over_contents(self):
        collection = ResourceCollection("some_query", self.collection_data, TestResourceCollection.TestResource.fetch)
        new_items = []
        index = 0
        for item in collection.items:
            self.assertEquals(TestResourceCollection.TestResource.items[index], item)
            new_items.append(item)
            index += 1

        self.assertEquals(5, len(new_items))

    def test_iterate_using_iterator_protocol(self):
        collection = ResourceCollection("some_query", self.collection_data, TestResourceCollection.TestResource.fetch)
        for test_elem, coll_elem in zip(self.TestResource.items, collection):
            self.assertEqual(test_elem, coll_elem)

    def test_ids_returns_array_of_ids(self):
        collection = ResourceCollection("some_query", self.collection_data, TestResourceCollection.TestResource.fetch)
        self.assertEqual(collection.ids, collection_data['search_results']['ids'])

    def test_ids_returns_array_of_ids(self):
        empty_collection_data = {
            "search_results": {
                "page_size": 2,
                "ids": []
             }
         }
        collection = ResourceCollection("some_query", empty_collection_data, TestResourceCollection.TestResource.fetch)
        self.assertEqual(collection.ids, [])

    @raises_with_regexp(UnexpectedError, "Unprocessable entity due to an invalid request")
    def test_no_search_results(self):
        bad_collection_data = { }
        collection = ResourceCollection("some_query", bad_collection_data, TestResourceCollection.TestResource.fetch)
