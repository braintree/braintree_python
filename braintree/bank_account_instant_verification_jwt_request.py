class BankAccountInstantVerificationJwtRequest(object):
    def __init__(self):
        self._business_name = None
        self._return_url = None
        self._cancel_url = None

    def business_name(self, business_name):
        self._business_name = business_name
        return self

    def return_url(self, return_url):
        self._return_url = return_url
        return self

    def cancel_url(self, cancel_url):
        self._cancel_url = cancel_url
        return self

        
    def get_business_name(self):
        return self._business_name
        
    def get_return_url(self):
        return self._return_url
        
    def get_cancel_url(self):
        return self._cancel_url
        

    def to_graphql_variables(self):
        input_data = {}
    
        if self._business_name is not None:
            input_data["businessName"] = self._business_name
        if self._return_url is not None:
            input_data["returnUrl"] = self._return_url
        if self._cancel_url is not None:
            input_data["cancelUrl"] = self._cancel_url

        return input_data