import random
import primality_testing.numbers_methods as nm

class ZeroKnowledgeProtocolAttack:
    def __init__(self, n, type='attacker', p=None, q=None) -> None:
        self.n = n

        if type == 'victim':
            self.p = p
            self.q = q

    def send_random_t_pow_2(self):
        self.t = random.randint(2, self.n - 1)
        y = pow(self.t, 2, self.n)

        return y

    def send_root(self, t_pow_2):
        X = nm.find_roots_blum_modules(t_pow_2, self.p, self.q)

        for root in X:
            if nm.legendre_symbol(root, self.p) and nm.legendre_symbol(root, self.q):
                return root

    def attack(self, root):
        if self.t != root and self.t != self.n - root:
            factor1 = nm.euclid((self.t + root) % self.n, self.n)
            factor2 = self.n // factor1
            return factor1, factor2
        else:
            return False