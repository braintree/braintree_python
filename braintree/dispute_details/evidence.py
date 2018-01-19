from braintree.attribute_getter import AttributeGetter

class DisputeEvidence(AttributeGetter):
    def __init__(self, attributes):
        if attributes.get("category") is not None:
            attributes["tag"] = attributes.pop("category")
        else:
            attributes["tag"] = None
        AttributeGetter.__init__(self, attributes)
