import random
import primality_testing.numbers_methods as nm
import RSA.RSAfuncs as rsaf

# Побудова криптосистеми
class RSA():
    def __init__(self, p=None, q=None, l=128, interval=False) -> None:
        if p is not None and q is not None:
            self.p, self.q = p, q
        else:
            self.p, self.q = rsaf.find_pair_of_good_primes(l, interval)
        self.generate_key_pair()

    def generate_key_pair(self):
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)

        self.e = 0x10001
        while nm.euclid(self.e, self.phi) != 1:
            self.e = random.randint(1, self.phi - 1)

        self.d = nm.inversed_element(self.e, self.phi)

        public_key = (self.n, self.e)

        return public_key

    def encrypt(self, M, public_key):
        n, e = public_key
        C = pow(M, e, n)

        return C

    def decrypt(self, C):
        M = pow(C, self.d, self.n)

        return M
        
    def sign(self, M):
        S = pow(M, self.d, self.n)

        return (M, S)

    def verify(self, signature, public_key):
        M, S = signature 
        n, e = public_key

        verification = pow(S, e, n)

        return M == verification

class RSA_protocol():
    def __init__(self, public_key=None, type='receiver') -> None:
        self.A = RSA()

        if public_key is not None:
            self.n1, self.e1 = public_key

        if type == 'sender':
            while self.A.n > self.n1:
                self.A = RSA(interval=(2, self.n1 ** 0.5))
                

        elif type == 'receiver' and public_key is not None:
            while self.A.n <= self.n1:
                self.A = RSA(interval=(self.n1, 2 * self.n1))

    def send_key(self, key):
        K1 = self.A.encrypt(key, (self.n1, self.e1))

        S = self.A.sign(key)[1]
        print('S = {}'.format(rsaf.to_hex(S)))
        S1 = self.A.encrypt(S, (self.n1, self.e1))

        return K1, S1
    
    def receive_key(self, message):
        K1, S1 = message

        key = self.A.decrypt(K1)
        S = self.A.decrypt(S1)

        check = self.A.verify((key, S), (self.n1, self.e1))

        return key, S, check