from typing import Union

# Схема Горнера 
def horner_pow(a: int, b: int, module: int) -> int:
    if b == 0: return 1

    degree = bin(b).lstrip('0').lstrip('b')
    y = 1
    for bit in degree:
        y = (y ** 2) % module
        y = (y * (a ** int(bit))) % module
    return y
    
# Знаходження НСД
def gcd(a: int, b: int) -> int:
    if a == 0: return b
    else: return gcd(b % a, a)

def euclid(a: int, b: int) -> tuple[int, list[int]]:
    if a > b:
        r_prev, r_cur = a, b
    else: r_prev, r_cur = b, a

    while r_cur != 0:
        r_next = r_prev % r_cur
        r_prev, r_cur = r_cur, r_next
    return r_prev

# Розширений алгоритм Евкліда
def extended_euclid(a: int, b: int) -> tuple[int, list[int]]:
    if a > b:
        r_prev, r_cur = a, b
    else: r_prev, r_cur = b, a
    q = []
    while r_cur != 0:
        q_cur = r_prev // r_cur
        q.append(q_cur)
        r_next = r_prev % r_cur
        r_prev, r_cur = r_cur, r_next
    return r_prev, q

# Пошук оберненого a за модулем n
def inversed_element(a: int, n: int) -> Union[int, bool]:
    u_prev, u_cur = 1, 0
    gcd, q = extended_euclid(a % n, n)
    if gcd == 1:
        for el in reversed(q):
            u_next = u_prev - el * u_cur
            u_prev, u_cur = u_cur, u_next
        return u_next % n if u_next > 0 else (u_next + n) % n
    return False

# Лема Безу (a < b)
def bezout(a: int, b: int) -> tuple[int, int]:
    if a < b:
        a, b = b, a
    u_prev, u_cur = 1, 0
    gcd, q = extended_euclid(a, b)
    if gcd == 1:
        for el in reversed(q):
            u_next = u_prev - el * u_cur
            u_prev, u_cur = u_cur, u_next
        return u_next, u_prev
    return False

# Обчислення символу Лежандра
def legendre_symbol(a: int, p: int) -> int:
    if p >= 2:
        if a >= p:
            a = a % p
        if a == 0:
            return 0
        elif a == 1:
            return 1
        elif a == -1 or a == p - 1:
            if ((p - 1) / 2) % 2 == 0: return 1 
            return -1
        elif a == 2:
            checker = horner_pow(p, 2, p)
            if ((checker - 1) / 8) % 2 == 0: return 1
            return -1
        else:
            result = horner_pow(a, (p - 1) // 2, p)
            return result if abs(result) < 2 else result - p
            
# Обчислення символу Якобі
def jacobi_symbol(a: int, n: int) -> int:
    a = a % n
    if a == 0: return 0


    if 0 < a < n and 4 < n:
        sign = 1
        result = a
        while True:
            if result == 0: return 0
            elif result == 1: return 1 * sign
            elif result == 2: 
                return ((-1) ** ((n ** 2 - 1) // 8)) * sign

            degree = 0
            while result % 2 == 0:
                result //= 2
                degree += 1

            if degree % 2 == 1: 
                sign *= (-1) ** ((n ** 2 - 1) // 8)

            if result == 1: return 1 * sign
            
            sign *= (-1) ** ((n - 1) * (result - 1) // 4)
            result, n = n % result, result
    
# Знаходження коренів рівняння y = x^2 mod n; n = p, q; p, q - числа Блюма
def find_roots_blum_modules(y, p, q):
    if jacobi_symbol(y, p * q) != 1:
        return False

    s_p = pow(y, (p + 1) // 4, p)
    s_q = pow(y, (q + 1) // 4, q)

    if p < q:
        u, v = bezout(p, q)
    else:
        v, u = bezout(q, p)

    n = p * q
    x1 = (u * p * s_q + v * q * s_p) % n
    x2 = (u * p * s_q - v * q * s_p) % n
    x3, x4 = n - x1, n - x2

    return [x1, x2, x3, x4]