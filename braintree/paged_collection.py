class PagedCollection(object):
    """A class representing a page of search results."""

    def __init__(self, query, results, klass):
        self.current_page_number = results["current_page_number"]
        self.collection = self.__extract_as_array(results, klass.__name__.lower())
        self.klass = klass
        self.page_size = results["page_size"]
        self.query = query
        self.total_items = results["total_items"]

    @property
    def first(self):
        if len(self.collection) == 0:
            return None
        return self.klass(self.collection[0])

    @property
    def items(self):
        for item in self.collection:
            yield self.klass(item)
        if not self.is_last_page:
            for item in self.next_page().items:
                yield item

    def next_page(self):
        """
        Returns another :class:`PagedCollection <braintree.paged_collection.PagedCollection>` representing the
        next page of results or None if this is the last page.
        """

        if self.is_last_page:
            return None
        return self.klass.search(self.query, self.current_page_number + 1)

    @property
    def current_page_size(self):
        """Returns the number of items on this page."""

        if self.is_last_page:
            return self.total_items % self.page_size
        else:
            return self.page_size

    @property
    def is_last_page(self):
        """Returns whether this is the last page of results."""

        return self.total_items == 0 or self.current_page_number == self.total_pages

    @property
    def total_pages(self):
        """Returns the total number of pages of search results."""

        total_pages = self.total_items / self.page_size
        if self.total_items % self.page_size != 0:
            total_pages += 1
        return total_pages

    def __extract_as_array(self, results, attribute):
        if not attribute in results:
            return []

        value = results[attribute]
        if type(value) != list:
            value = [value]
        return value

    def __getitem__(self, index):
        return self.items[index]
