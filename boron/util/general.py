import random
import string
from boron.util.db import query
from flask import abort


def rnd_string(length):
    return "".join(random.choices(string.ascii_letters, k=length))


def rnd_stringu(length):
    return rnd_string(length).upper()


def get_developer(session):
    res = query(
        "SELECT * FROM developers WHERE session = :session", {"session": session}
    )
    if len(res) == 1:
        return res[0]
    return abort(401)


def gen_license():
    return f"{rnd_stringu(5)}-{rnd_stringu(2)}B0R0N{rnd_stringu(2)}-{rnd_stringu(5)}"
