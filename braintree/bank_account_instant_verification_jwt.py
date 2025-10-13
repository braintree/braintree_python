from braintree.attribute_getter import AttributeGetter

class BankAccountInstantVerificationJwt(AttributeGetter):
    def __init__(self, jwt):
        self.jwt = jwt

    @property
    def jwt(self):
        return self._jwt

    @jwt.setter
    def jwt(self, value):
        self._jwt = value