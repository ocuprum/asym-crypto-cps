from typing import Union

# Знаходження НСД
def gcd(a: int, b: int) -> int:
    if a == 0: return b
    else: return gcd(b % a, a)

# Схема Горнера 
''' 
def horner_pow(a: int, b: int, module: int) -> int:
    if b == 0: return 1

    degree = bin(b).lstrip('0').lstrip('b')
    y = 1
    for bit in degree:
        y = (y ** 2) % module
        y = (y * (a ** int(bit))) % module
    return y
'''

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
        return u_next if u_next >= 0 else u_next + n
    return False