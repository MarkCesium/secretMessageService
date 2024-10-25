import hashlib
from time import time


def get_message_hash(text: str, salt: str) -> str:
    return hashlib.sha256(
        text.encode("UTF-8") + salt.encode("UTF-8") + str(time()).encode("UTF-8"),
    ).hexdigest()
