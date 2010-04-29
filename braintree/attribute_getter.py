class AttributeGetter(object):
    def __init__(self, attributes={}):
        for key, val in attributes.iteritems():
            setattr(self, key, val)
