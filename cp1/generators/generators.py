
import time
import math
import random
from generators.LFSR import LFSR
from generators.Geffe import Geffe

def built_in(N):
    return bin(random.getrandbits(N))[2:].zfill(N)

def gen_initial(N):
    result = [int(bit) for bit in built_in(N)]

    return result

def lemer_low(N):
    m = 1 << 32
    a = (1 << 16) + 1
    c = 119

    x = int(built_in(32), 2)

    result = ''
    for _ in range(N // 8):
        x_str = bin(x)[2:][-8:].zfill(8)
        x = (a * x + c) % m
        result += x_str

    return result

def lemer_high(N):
    m = 1 << 32
    a = (1 << 16) + 1
    c = 119

    x = int(built_in(32), 2)

    result = ''
    for _ in range(N // 8):
        x_str = bin(x)[2:][:8].zfill(8)
        x = (a * x + c) % m
        result += x_str

    return result

def l20(N):
    lfsr = LFSR(gen_initial(20), [0, 11, 15, 17])

    result = ''
    for _ in range(N): 
        result += str(lfsr.next())

    return result

def l89(N):
    lfsr = LFSR(gen_initial(89), [0, 51])

    result = ''
    for _ in range(N):
        result += str(lfsr.next())

    return result

def geffe(N):
    l1 = LFSR(gen_initial(11), [0, 2])
    l2 = LFSR(gen_initial(9), [0, 1, 3, 4])
    l3 = LFSR(gen_initial(10), [0, 3])

    gen = Geffe(l1, l2, l3)
    result = ''
    for _ in range(N): 
        result += str(gen.next())

    return result

def right_shift(n):
    n = bin(n)[2:].zfill(32)
    shifted_n = n[-1] + n[0:-1]

    return int(shifted_n, 2)

def left_shift(n):
    n = bin(n)[2:].zfill(32)
    shifted_n = n[1:] + n[0]

    return int(shifted_n, 2)

def wolfram(N):
    r = int(built_in(32), 2)

    result = ''
    for _ in range(N):
        result += str(r % 2) 
        r = right_shift(r) ^ (r | left_shift(r))

    return result
    
def librarian(fname, N):
    fhandle = open(fname)
    bs = bytes(fhandle.read(), 'utf-8')[:(N // 8)]
    bs = [bin(b)[2:].zfill(8) for b in bs]
    return ''.join(bs)    

def bm(N):
    p = int('CEA42B987C44FA642D80AD9F51F10457690DEF10C83D0BC1BCEE12FC3B6093E3', 16)
    a = int('5B88C41246790891C095E2878880342E88C79974303BD0400B090FE38A688356', 16)
    q = int('675215CC3E227D3216C056CFA8F8822BB486F788641E85E0DE77097E1DB049F1', 16)

    T = random.randint(0, p-1)
    
    result = ''
    for _ in range(N):
        x = 1 if T < q else 0
        result += str(x)
        T = pow(a, T, p)
    
    return result

def bm_bytes(N):
    p = int('CEA42B987C44FA642D80AD9F51F10457690DEF10C83D0BC1BCEE12FC3B6093E3', 16)
    a = int('5B88C41246790891C095E2878880342E88C79974303BD0400B090FE38A688356', 16)
    q = int('675215CC3E227D3216C056CFA8F8822BB486F788641E85E0DE77097E1DB049F1', 16)

    T = random.randint(0, p-1)
    
    result = ''
    for _ in range(N // 8):
        k = T * 128 / q
        if k == math.floor(k): k -= 1
        else: k = math.floor(k)

        result += bin(k)[2:].zfill(8)
        T = pow(a, T, p)
    
    return result
    
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

def bbs_bytes(N):
    p = int('D5BBB96D30086EC484EBA3D7F9CAEB07', 16)
    q = int('425D2B9BFDB25B9CF6C416CC6E37B59C1F', 16)
    n = p * q

    r = random.randint(2, n-1)

    result = ''
    for _ in range(N // 8):
        r = pow(r, 2, n)
        x = bin(r % 256)[2:].zfill(8)
        result += str(x)

    return result