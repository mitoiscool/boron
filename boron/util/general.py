import random
import string
def rnd_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))
