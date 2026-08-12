import re

# Allowlist of the characters that make up a Braintree id/token. Excluding "."
# (along with "/" and "%") makes path-traversal segments such as ".." or
# encoded variants impossible to construct.
VALID_PATH_SEGMENT_REGEX = re.compile(r"\A[A-Za-z0-9_-]+\Z")

def is_invalid_path_segment(value):
    if not isinstance(value, str):
        return True
    return not VALID_PATH_SEGMENT_REGEX.search(value)
