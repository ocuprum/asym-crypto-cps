import random
from typing import Union
import primality_testing.primes_to_300000 as pttt
import primality_testing.numbers_methods as nm
import decimal as dec

# Метод пробних ділень (повертає False, якщо число просте)
def trial_division(n: int, B: int=10) -> Union[int, bool]:
    sq_n = int(dec.Decimal(n) ** dec.Decimal(1 / 2))
    nums = [int(num) for num in str(n)[::-1]]

    for prime in pttt.primes:
        if prime <= sq_n and prime <= 47:
            r = 1
            poss_n = 0
            for num in nums:
                poss_n += (num * r)
                r = (r * B) % prime
            if poss_n % prime == 0: return prime
    return False

# Тест Міллера-Рабіна на простоту
def miller_rabin(p: int, k: int=5) -> bool:
    if p == 2: return True
    if p > 2 and k > 0:
        d = p - 1
        s = 0
        while d % 2 == 0:
            s += 1
            d //= 2
        
        counter = 0
        is_strong_pseudoprime = False
        while counter <= k:
            rand_x = random.randint(2, p - 1)
            if nm.euclid(rand_x, p) == 1: 
                poss_pseudoprime = nm.horner_pow(rand_x, d, p)
                if poss_pseudoprime == 1 or poss_pseudoprime == p-1 or poss_pseudoprime == -1:
                    is_strong_pseudoprime = True
                else: 
                    x = poss_pseudoprime
                    for _ in range(s):
                        x = (x ** 2) % p
                        if x == p-1 or x == -1: 
                            is_strong_pseudoprime = True
                            break
                        elif x == 1: 
                            return False
                if is_strong_pseudoprime: 
                    counter += 1
                    continue
                return False
            return False
        return True