import hashlib


def hash_key(string_key: str):
    return hashlib.sha256(string_key.encode('utf-8')).hexdigest()
