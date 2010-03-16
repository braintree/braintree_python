class UnexpectedError(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return text
