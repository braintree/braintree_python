import hashlib
import hmac

class Crypto:
    @staticmethod
    def hmac_hash(secret_key, content):
        return hmac.new(hashlib.sha1(secret_key).digest(), content, hashlib.sha1).hexdigest()
