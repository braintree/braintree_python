import urllib
from braintree.util.crypto import Crypto

class SignatureService(object):

    def __init__(self, private_key, hashfunc=Crypto.sha1_hmac_hash):
        self.private_key = private_key
        self.hmac_hash = hashfunc

    def sign(self, data):
      url_encoded_data = urllib.urlencode(data)
      return "%s|%s" % (self.hash(url_encoded_data), url_encoded_data)

    def hash(self, data):
      return self.hmac_hash(self.private_key, data)
