class ArgumentError(Exception):
    def __init__(self, text):
        self.test = text

    def __str__(self):
        return "ArgumentError: " + self.text
