import random
import string


def rnd_str(length: int):
    return "".join(random.choices(string.ascii_letters, k=length))


def rnd_str_u(length: int):
    return rnd_str(length).upper()


def gen_license(prefix: str = "BORON"):
    assert len(prefix) == 5
    return f"{prefix}-{rnd_str_u(4)}-{rnd_str_u(4)}-{rnd_str_u(4)}-{rnd_str_u(4)}"
