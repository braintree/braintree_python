import warnings

class DeprecationUtil(object):
    @staticmethod
    def deprecation(message):
        warnings.warn(message, DeprecationWarning, stacklevel=2)
