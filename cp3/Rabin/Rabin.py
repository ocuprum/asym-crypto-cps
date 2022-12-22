import random
import RNG.rng as rng
import Rabin.RabinFuncs as rabinf
import primality_testing.numbers_methods as nm

class Rabin:
    def __init__(self, l=256, interval=False) -> None:
        self.__generate_key_pair(l, interval)

    def __generate_key_pair(self, l, interval):
        self.p, self.q = rabinf.find_pair_of_blum_primes(l, interval)

        self.n = self.p * self.q
        self.b = random.randint(0, self.n - 1)

        public_key = (self.n, self.b)

        return public_key

    def __format(self, message, n):
        hex_m = rabinf.to_hex(message)

        l_n = len(rabinf.to_hex(n)) // 2
        l_message = len(hex_m) // 2

        if l_message > l_n - 10:
            return False
        
        r = rabinf.to_hex(int('1' + rng.bbs(63), 2))

        x = 'FF' + hex_m.zfill((l_n - 10) * 2) + r
        return int(x, 16) 

    def encrypt(self, message, public_key):
        n, b = public_key
        x = self.__format(message, n)
        if x is False:
            return x

        y = (x * (x + b)) % n
        inv_2 = nm.inversed_element(2, n)
        c1 = ((x + b * inv_2) % n) % 2
        c2 = nm.jacobi_symbol(x + b * inv_2, n)

        return y, c1, c2

    def __deformat(self, x):
        message = rabinf.to_hex(x).lstrip('0')[2:][:-16]
        return int(message, 16)

    def __check_root(self, root, c1, c2):
        inv_2 = nm.inversed_element(2, self.n)
        real_c1 = ((root + self.b * inv_2) % self.n) % 2
        real_c2 = nm.jacobi_symbol(root + self.b * inv_2, self.n)

        real_c2 = 1 if real_c2 == 1 else 0
        if  c1 == real_c1 and c2 == real_c2:
            return True
        return False

    def decrypt(self, ciphertext):
        y, c1, c2 = ciphertext

        inv_2 = nm.inversed_element(2, self.n)
        inv_4 = nm.inversed_element(4, self.n)
        X = nm.find_roots_blum_modules(y + (self.b ** 2) * inv_4, self.p, self.q)
        if X is False:
            print('Неможливо знайти корені') 
            return -1
        X = [(root - (self.b * inv_2)) % self.n for root in X]

        x = None
        for root in X:
            if self.__check_root(root, c1, c2):
                x = root
                break

        if x is not None:
            message = self.__deformat(x)
        else:
            print('Ні один з коренів не є ВТ')
            return -1
        return message

    def sign(self, message):
        x = 0
        while nm.legendre_symbol(x, self.p) != 1 or nm.legendre_symbol(x, self.q) != 1:
            x = self.__format(message, self.n)

        X = nm.find_roots_blum_modules(x, self.p, self.q)
        return random.choice(X)

    def verify(self, signature, public_key):
        m, s = signature
        n, _ = public_key

        x = pow(s, 2, n)
        
        return m == self.__deformat(x)