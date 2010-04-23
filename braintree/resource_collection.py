class ResourceCollection(object):
    """
    A class representing results from a search.  Iterate over the results by calling items::

        results = braintree.Transaction.search("411111")
        for transaction in results.items:
            print transaction.id
    """

    def __init__(self, query, results, klass):
        self.__current_page_number = results["current_page_number"]
        self.__collection = self.__extract_as_array(results, klass.__name__.lower())
        self.__klass = klass
        self.__page_size = results["page_size"]
        self.__query = query
        self.__total_items = results["total_items"]

    @property
    def approximate_size(self):
        """
        Returns the approximate size of the results.  The size is approximate due to race conditions when pulling
        back results.  Due to its inexact nature, approximate_size should be avoided.
        """
        return self.__total_items

    @property
    def first(self):
        """ Returns the first item in the results. """
        if len(self.__collection) == 0:
            return None
        return self.__klass(self.__collection[0])

    @property
    def items(self):
        """ Returns a generator allowing iteration over all of the results. """
        for item in self.__collection:
            yield self.__klass(item)
        if not self.__is_last_page:
            for item in self.__next_page().items:
                yield item

    def __extract_as_array(self, results, attribute):
        if not attribute in results:
            return []

        value = results[attribute]
        if type(value) != list:
            value = [value]
        return value

    @property
    def __is_last_page(self):
        return self.__total_items == 0 or self.__current_page_number == self.__total_pages

    def __next_page(self):
        if self.__is_last_page:
            return None
        return self.__klass.search(self.__query, self.__current_page_number + 1)

    @property
    def __total_pages(self):
        total_pages = self.__total_items / self.__page_size
        if self.__total_items % self.__page_size != 0:
            total_pages += 1
        return total_pages
