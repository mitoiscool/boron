import random
import string
from boron.util.db import query
from flask import abort

def rnd_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def get_developer(session):
    try:
        return query("SELECT * FROM developers WHERE session = ?", (session,)[0])
    except:
        abort(401)
    