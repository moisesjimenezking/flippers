import random
import string

def generated(long):
    charartes = string.ascii_letters
    strings = ''.join(random.choice(charartes) for _ in range(long))
    return strings