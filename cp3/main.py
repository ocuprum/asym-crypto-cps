import Rabin.Rabin as rabin
from Rabin.RabinFuncs import to_hex
import ZeroKnowledgeProtocolAttack.ZKPA as zkpa

while True:
    print('1 - Ввести ServerKey')
    print('2 - Створити нового користувача')
    print('3 - Cтворити новий протокол')
    print('4 - Створити двох абонентів')
    print('0 - Завершити роботу')

    answer = int(input('\nОберіть потрібний варіант: '))
    print('----------------------------\n')

    if answer == 0: break

    elif answer == 1:
        server_key_n = input('Введіть Server Key - n: ')
        server_key_b = input('Введіть Server Key - b: ')
        server_key_n, server_key_b = int(server_key_n.lower(), 16), int(server_key_b.lower(), 16)
        print()

    elif answer == 2:
        A = rabin.Rabin()
        print('Створено нового користувача RabinExtended')

        while True:
            print('1 - Розшифрувати повідомлення, отримане від сервера')
            print('2 - Зашифрувати повідомлення для сервера')
            print('3 - Надати серверу повідомлення на підпис')
            print('4 - Підписати повідомлення користувача')
            print('0 - Завершити роботу з цим користувачем')

            answer = int(input('\nОберіть потрібний варіант: '))
            print('----------------------------\n')

            if answer == 0:
                break
            
            elif answer == 1:
                print('Відкритий ключ користувача - n: {}'.format(to_hex(A.n)))
                print('Відкритий ключ користувача - b: {}\n'.format(to_hex(A.b)))
                ciphertext = int(input('Введіть ШТ, отриманий від сервера: '), 16)
                c1 = int(input('Введіть c1: '))
                c2 = int(input('Введіть c2: '))
                message = A.decrypt((ciphertext, c1, c2))
                if message == -1:
                    print('Недійсний ШТ')
                else:
                    print('Користувач розшифрував повідомлення: {}'.format(to_hex(message)))

            elif answer == 2:
                message = int(input('Введіть повідомлення: '), 16)
                y, c1, c2 = A.encrypt(message, (server_key_n, server_key_b))
                c2 = 1 if c2 == 1 else 0
                print('Шифротекст для сервера: {}'.format(to_hex(y)))
                print('c1: {}'.format(c1))
                print('c2: {}'.format(c2))

            elif answer == 3:
                message = int(input('Введіть повідомлення: ').lower(), 16)
                sign = int(input('Введіть підпис сервера: ').lower(), 16)
                print('Перевірка підпису сервера: {}'.format(bool(A.verify((message, sign), (server_key_n, server_key_b)))))

            elif answer == 4:
                message = int(input('Введіть повідомлення: ').lower(), 16)
                print('Відкритий ключ користувача - n: {}'.format(to_hex(A.n)))
                sign = A.sign(message)
                print('Підпис користувача: {}'.format(to_hex(sign)))

            print()
    
    elif answer == 3:
        n = int(input('Введіть n: ').lower(), 16)
        protocolS = zkpa.ZeroKnowledgeProtocolAttack(n)
        print()
        print('Створено новий протокол')

        while True:
            print('1 - Надіслати Y')
            print('0 - Завершити роботу з цим протоколом')

            answer = int(input('\nОберіть потрібний варіант: '))
            print('----------------------------\n')

            if answer == 0:
                break

            elif answer == 1:
                roots = False
                i = 1
                while not roots:
                    print('Спроба №{}'.format(i))
                    print('---------')
                    Y = protocolS.send_random_t_pow_2()
                    print('Випадкове значення для сервера: {}\n'.format(to_hex(Y)))
                    root = int(input('Введіть квадратний корінь, отриманий від сервера: ').lower(), 16)
                    roots = protocolS.attack(root)
                    if roots is False:
                        print()
                        print('[НЕУСПІШНА АТАКА]')
                        print()

                    else:
                        p, q = roots
                        print()
                        print('[АТАКА УСПІШНА]')
                        print('Секретний ключ сервера - p: {}\n'.format(to_hex(p)))
                        print('Секретний ключ сервера - q: {}\n'.format(to_hex(q)))
                        print('Перевірка: n = p * q -> {}\n'.format(protocolS.n == p * q))
                    i += 1

            print()
    

    elif answer == 4:
        A = rabin.Rabin()
        B = rabin.Rabin()

        print('Прості числа')
        print('------------\n')
        print('A: p = {}, q = {}'.format(to_hex(A.p), to_hex(A.q)))
        print('B: p = {}, q = {}'.format(to_hex(B.p), to_hex(B.q)))
        print()

        print('Параметри')
        print('---------\n')
        print('A: n = {}, b = {}'.format(to_hex(A.n), to_hex(A.b)))
        print('B: n = {}, b = {}'.format(to_hex(B.n), to_hex(B.b)))
        print()

        #TODO: change from here
        plaintext = int(input('Введіть повідомлення: '), 16)
        while plaintext >= A.n or plaintext >= B.n:
            print('Повідомленя більше за n!')
            plaintext = int(input('Введіть повідомлення: '), 16)

        print('Відкритий текст: {}'.format(to_hex(plaintext)))
        print('-------------------------------------\n')
        print('Абонент A:')
        ciphertext, c1, c2 = A.encrypt(plaintext, (B.n, B.b))
        print('Шифротекст: {}'.format(to_hex(ciphertext)))
        print('c1 = {}'.format(c1))
        print('c2 = {}'.format(c2))
        print('Підпис: {}'.format(to_hex(A.sign(plaintext))))
        print()
        print('Абонент B:')
        ciphertext, c1, c2 = B.encrypt(plaintext, (A.n, A.b))
        print('Шифротекст: {}'.format(to_hex(ciphertext)))
        print('c1 = {}'.format(c1))
        print('c2 = {}'.format(c2))
        print('Підпис: {}'.format(to_hex(B.sign(plaintext))))
        print('\n')