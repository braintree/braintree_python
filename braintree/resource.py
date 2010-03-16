from braintree.attribute_getter import AttributeGetter

class Resource(AttributeGetter):
    @staticmethod
    def verify_keys(params, signature):
        allowed_keys = Resource.__flattened_signature(signature)
        params_keys = Resource.__flattened_params_keys(params)

        for key in params_keys:
            if not key in allowed_keys:
                raise KeyError(key + " is not an allowed key")

    @staticmethod
    def __flattened_params_keys(params):
        keys = []
        for key, val in params.iteritems():
            keys.append(key)
            if type(val) == dict:
                keys += Resource.__flattened_params_keys(val)
        return keys

    @staticmethod
    def __flattened_signature(signature):
        flat_sig = []
        for item in signature:
            if type(item) == dict:
                for key, val in item.iteritems():
                    flat_sig.append(key)
                    flat_sig += Resource.__flattened_signature(val)
            else:
                flat_sig.append(item)
        return flat_sig
