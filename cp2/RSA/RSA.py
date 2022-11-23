import random
import RNG.rng as rng
import primality_testing.primality_tests as pt

def find_prime(l=False, interval=False):
    test = False 
    while not test:         
        if interval:
            b1, b2 = interval
            l = len(bin(random.randint(b1, b2))[2:])
        
        poss_prime = int(rng.l20(l), 2)
        if interval and (not b1 <= poss_prime <= b2): continue
        test = pt.trial_division(poss_prime, 2)
        if test: test = pt.miller_rabin(poss_prime)

    return poss_prime