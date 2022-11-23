import random
from RNG.LFSR import LFSR

def built_in(N):
    return bin(random.getrandbits(N))[2:].zfill(N)

def gen_initial(N):
    result = [int(bit) for bit in built_in(N)]

    return result
    
def l20(N):
    lfsr = LFSR(gen_initial(20), [0, 11, 15, 17])

    result = ''
    for _ in range(N): 
        result += str(lfsr.next())

    return result