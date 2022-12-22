from math import log2
import random
import RNG.rng as rng
import primality_testing.primality_tests as pt

def to_hex(number):
    x = hex(number).lstrip('0').lstrip('x').upper()
    if len(x) % 2 == 1:
        x.zfill(len(x) + 1)
    return x

# Пошук простого числа
def find_prime(l=256, interval=False, k=10):
    counter = 0
    test = False 

    if interval:
        b1, b2 = interval

    while not test:        
        if interval:
            if counter == k:
                b2 = 2 * b1 - 2
            l = len(bin(random.randint(b1, b2))[2:])
        
        poss_prime = int(rng.bbs(l), 2)
        if interval and (not b1 <= poss_prime <= b2): continue
        test = pt.trial_division(poss_prime, 2)
        if test: test = pt.miller_rabin(poss_prime)

    return poss_prime

# Пошук простого числа Блюма
def find_blum_prime(l=256, interval=False):
    prime = find_prime(l, interval)

    while prime % 4 != 3:
        prime = find_prime(l, interval)
    
    return prime

# Пошук пари простих чисел Блюма
def find_pair_of_blum_primes(l=256, interval=False):
    p = find_blum_prime(l, interval)
    q = find_blum_prime(l, interval)

    while p == q:
        q = find_blum_prime(l, interval)

    return p, q