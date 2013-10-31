import urllib
from braintree.util.crypto import Crypto

class SignatureService(object):

    def __init__(self, private_key, digest=Crypto):
        self.private_key = private_key
        self.digest = digest

    def sign(self, data):
      url_encoded_data = urllib.urlencode(data)
      return "%s|%s" % (self.hash(url_encoded_data), url_encoded_data)

    def hash(self, data):
      return self.digest.hmac_hash(self.private_key, data)
