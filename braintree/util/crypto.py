import hashlib
import hmac

class Crypto:
    @staticmethod
    def hmac_hash(secret_key, content):
        return hmac.new(hashlib.sha1(secret_key).digest(), content, hashlib.sha1).hexdigest()

    @staticmethod
    def secure_compare(left, right):
        if left == None or right == None:
            return False

        left_bytes = bytearray(left)
        right_bytes = bytearray(right)

        if len(left_bytes) != len(right_bytes):
            return False

        result = 0
        for left_byte, right_byte in zip(left_bytes, right_bytes):
            result |= left_byte ^ right_byte
        return result == 0
