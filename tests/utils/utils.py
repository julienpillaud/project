import random
import string


def random_string(size: int = 32, upper: bool = False) -> str:
    string_random = "".join(random.choices(string.ascii_lowercase, k=size))
    return string_random.upper() if upper else string_random


def random_email() -> str:
    return f"{random_string()}@{random_string()}.com"
