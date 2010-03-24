#import braintree.transaction

class PagedCollection(object):
    def __init__(self, query, collection, klass, klass_name):
        self.current_page_number = collection["current_page_number"]
        self.page_size = collection["page_size"]
        self.total_items = collection["total_items"]
        self.items = [klass(item) for item in collection[klass_name]]
        self.klass = klass
        self.query = query

    def next_page(self):
        return self.klass.search(self.query, self.current_page_number + 1)

    def __getitem__(self, index):
        return self.items[index]
