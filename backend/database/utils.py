import datetime
import random
import string


def current_datetime() -> str:
    return str(datetime.datetime.utcnow())


def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


def generate_salt(salt_length: int = 8):
    valid_chars = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rng = random.SystemRandom()
    salt = []
    for _ in range(salt_length):
        choice = rng.randint(0, 63)
        salt.append(valid_chars[choice])
    return "".join(salt)