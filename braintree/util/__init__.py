class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable
