import hashlib
import hmac
import six


class Crypto:
    @staticmethod
    def hmac_hash(secret_key, content):
        if isinstance(secret_key, six.string_types):
            secret_key = secret_key.encode('ascii')
        if isinstance(content, six.string_types):
            content = content.encode('ascii')
        return hmac.new(hashlib.sha1(secret_key).digest(), content, hashlib.sha1).hexdigest()

    @staticmethod
    def secure_compare(left, right):
        if left is None or right is None:
            return False

        left_bytes = [ord(char) for char in left]
        right_bytes = [ord(char) for char in right]

        if len(left_bytes) != len(right_bytes):
            return False

        result = 0
        for left_byte, right_byte in zip(left_bytes, right_bytes):
            result |= left_byte ^ right_byte
        return result == 0
