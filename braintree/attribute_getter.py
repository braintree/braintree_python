class AttributeGetter(object):
    def __init__(self, attributes={}):
        self._setattrs = []
        for key, val in attributes.items():
            setattr(self, key, val)
            self._setattrs.append(key)

    def __repr__(self, detail_list=None):
        if detail_list is None:
            detail_list = self._setattrs

        details = ", ".join("%s: %r" % (attr, getattr(self, attr))
                                for attr in detail_list
                                    if hasattr(self, attr))
        return "<%s {%s} at %d>" % (self.__class__.__name__, details, id(self))
