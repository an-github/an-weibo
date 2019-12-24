import random
from hashlib import sha256


def gen_password(user_password):
    bin_password = user_password.encode('utf8')
    hash_value = sha256(bin_password).hexdigest()
    salt = '%x' % random.randint(0x10000000, 0xffffffff)
    safe_password = salt + hash_value
    return safe_password


def check_password(user_password, safe_password):

    bin_password = user_password.encode('utf8')
    hash_value = sha256(bin_password).hexdigest()

    return hash_value == safe_password[8:]
