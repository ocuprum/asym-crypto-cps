import random
from RNG.LFSR import LFSR

def bbs(N):
    p = int('D5BBB96D30086EC484EBA3D7F9CAEB07', 16)
    q = int('425D2B9BFDB25B9CF6C416CC6E37B59C1F', 16)
    n = p * q

    r = random.randint(2, n-1)

    result = ''
    for _ in range(N):
        r = pow(r, 2, n)
        x = r % 2
        result += str(x)

    return result