import random
import RNG.rng as rng
import primality_testing.primality_tests as pt

def to_hex(number):
    f = 4 - len(str(number)) % 4
    return hex(number).lstrip('0').lstrip('x').upper().zfill(f)

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

# Пошук "гарного" простого числа виду p = 2 * i * p' + 1
def find_good_prime(l=256, interval=False):
    prime = find_prime(l, interval)
    
    good_prime = 1 + 2 * prime
    while not pt.miller_rabin(good_prime):
        good_prime += 2 * prime

    return good_prime

# Пошук пари "гарних" простих 
def find_pair_of_good_primes(l=1024, interval=False):
    p = find_good_prime(l, interval)
    q = find_good_prime(l, interval)

    while p == q:
        q = find_good_prime(l, interval)

    return (p, q)