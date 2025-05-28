def Experimental(cls):
    """
    Experimental features may change at any time.

    Decorator to mark a class as experimental.
    Adds an '_is_experimental' attribute to the class.
    """
    cls._is_experimental = True
    return cls