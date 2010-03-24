#import braintree.transaction

class PagedCollection(object):
    def __init__(self, collection, klass, klass_name):
        self.current_page_number = collection["current_page_number"]
        self.page_size = collection["page_size"]
        self.total_items = collection["total_items"]
        self.items = [klass(item) for item in collection[klass_name]]

    def __getitem__(self, index):
        return self.items[index]
