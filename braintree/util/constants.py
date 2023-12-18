#NEXT_MAJOR_VERSION we can change all Constants to enums, not sure if we'll still need this
class Constants(object):
    @staticmethod
    def get_all_constant_values_from_class(klass):
        return [klass.__dict__[item] for item in dir(klass) if not item.startswith("__")]
    def get_all_enum_values(enum_class):
        return [item.value for item in enum_class]
