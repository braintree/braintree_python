import re
from braintree.attribute_getter import AttributeGetter

class Resource(AttributeGetter):
    @staticmethod
    def verify_keys(params, signature):
        allowed_keys = Resource.__flattened_signature(signature)
        params_keys = Resource.__flattened_params_keys(params)

        invalid_keys = [key for key in params_keys if key not in allowed_keys]
        invalid_keys = Resource.__remove_wildcard_keys(allowed_keys, invalid_keys)

        if len(invalid_keys) > 0:
            keys_string = ", ".join(invalid_keys)
            raise KeyError("Invalid keys: " + keys_string)

    @staticmethod
    def __flattened_params_keys(params, parent=None):
        keys = []
        for key, val in params.iteritems():
            full_key = parent + "[" + key + "]" if parent else key
            if type(val) == dict:
                keys += Resource.__flattened_params_keys(val, full_key)
            else:
                keys.append(full_key)
        return keys

    @staticmethod
    def __flattened_signature(signature, parent=None):
        flat_sig = []
        for item in signature:
            if type(item) == dict:
                for key, val in item.iteritems():
                    full_key = parent + "[" + key + "]" if parent else key
                    flat_sig += Resource.__flattened_signature(val, full_key)
            else:
                full_key = parent + "[" + item + "]" if parent else item
                flat_sig.append(full_key)
        return flat_sig

    @staticmethod
    def __remove_wildcard_keys(allowed_keys, invalid_keys):
        wildcard_keys = [re.sub("\\[__any_key__\\]\Z", "", key) for key in allowed_keys if re.search("\\[__any_key__\\]", key)]
        new_keys = []
        for key in invalid_keys:
            if len([match for match in wildcard_keys if re.match(match, key)]) == 0:
                new_keys.append(key)
        return new_keys

