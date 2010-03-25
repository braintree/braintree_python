class AttributeGetter(object):
    def __init__(self, attributes={}):
        for key, val in attributes.iteritems():
            self.__dict__[key] = val
