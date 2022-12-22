import Rabin.Rabin as rabin
import RNG.rng as rng
from Rabin.RabinFuncs import to_hex

while True:
    print('1 - Ввести ServerKey')
    print('2 - Створити нового користувача')
    print('3 - Cтворити новий протокол')
    #print('4 - Створити двох абонентів')
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
        protocolS = rsa.RSA_protocol((server_key_n, server_key_e), type='sender')
        protocolR = rsa.RSA_protocol((server_key_n, server_key_e), type='receiver')
        print('Створено новий протокол')

        while True:
            print('1 - Надіслати ключ')
            print('2 - Отримати ключ')
            print('0 - Завершити роботу з цим протоколом')

            answer = int(input('\nОберіть потрібний варіант: '))
            print('----------------------------\n')

            if answer == 0:
                break

            elif answer == 1:
                message = int(input('Введіть секретний ключ: ').lower(), 16)
                while not 0 < message < protocolS.A.n:
                    print('Введене некоректне значення ключа')
                    message = int(input('Введіть секретний ключ: ').lower(), 16)
                K1, S1 = protocolS.send_key(message)
                print('Зашифрований ключ: {}'.format(to_hex(K1)))
                print('Підпис користувача: {}'.format(to_hex(S1)))
                print('Відкритий ключ користувача - n: {}'.format(to_hex(protocolS.A.n)))
                print('Відкритий ключ користувача - e: {}\n'.format(to_hex(protocolS.A.e)))

            elif answer == 2:
                print('Відкритий ключ користувача - n: {}'.format(to_hex(protocolR.A.n)))
                print('Відкритий ключ користувача - e: {}\n'.format(to_hex(protocolR.A.e)))
                K1 = int(input('Введіть зашифрований ключ: ').lower(), 16)
                S1 = int(input('Введіть підпис: ').lower(), 16)
                print()
                key, S, check = protocolR.receive_key((K1, S1))
                print('Зашифрований ключ: {}'.format(to_hex(key)))
                print('Підпис користувача: {}'.format(to_hex(S)))
                print('Перевірка підпису: {}'.format(check))

            print()
    
    '''
    elif answer == 4:
        protocolR = rsa.RSA_protocol(type='receiver')
        protocolS = rsa.RSA_protocol(public_key=(protocolR.A.n, protocolR.A.e), type='sender')
        protocolR.n1, protocolR.e1 = protocolS.A.n, protocolS.A.e

        print('A.n <= B.n: {}'.format(protocolS.A.n <= protocolR.A.n))
        print()

        print('Прості числа')
        print('------------\n')
        print('A: p = {}, q = {}'.format(to_hex(protocolS.A.p), to_hex(protocolS.A.q)))
        print('B: p = {}, q = {}'.format(to_hex(protocolR.A.p), to_hex(protocolR.A.q)))
        print()

        print('Параметри')
        print('---------\n')
        print('A: n = {}, e = {}, d = {}'.format(to_hex(protocolS.A.n), to_hex(protocolS.A.e), to_hex(protocolS.A.d)))
        print('B: n = {}, e = {}, d = {}'.format(to_hex(protocolR.A.n), to_hex(protocolR.A.e), to_hex(protocolR.A.d)))
        print()

        plaintext = int(input('Введіть повідомлення: '), 16)
        while plaintext >= protocolS.A.n or plaintext >= protocolR.A.n:
            print('Повідомленя більше за n!')
            plaintext = int(input('Введіть повідомлення: '), 16)

        print('Відкритий текст: {}'.format(to_hex(plaintext)))
        print('-------------------------------------\n')
        print('Абонент A:')
        print('Шифротекст: {}'.format(to_hex(protocolS.A.encrypt(plaintext, (protocolR.A.n, protocolR.A.e)))))
        print('Підпис: {}'.format(to_hex(protocolS.A.sign(plaintext)[1])))
        print()
        print('Абонент B:')
        print('Шифротекст: {}'.format(to_hex(protocolR.A.encrypt(plaintext, (protocolS.A.n, protocolS.A.n)))))
        print('Підпис: {}'.format(to_hex(protocolR.A.sign(plaintext)[1])))
        print('\n')

        print('Протокол розсилання ключів')
        print('--------------------------\n')

        print('1) A формує повідомлення:')
        secret_key = int(input('Введіть секретний ключ: '), 16)
        while secret_key >= protocolS.A.n:
            print('Повідомленя більше за n!')
            secret_key = int(input('Введіть секретний ключ: '), 16)
        print('Секретний ключ: {}'.format(to_hex(secret_key)))
        k1, S1 = protocolS.send_key(secret_key)
        print('k1 = {}'.format(to_hex(k1)))
        print('S1 = {}'.format(to_hex(S1)))
        print()

        print('2) B знаходить:')
        k, S, check = protocolR.receive_key((k1, S1))
        print('k = {}'.format(to_hex(k)))
        print('S = {}'.format(to_hex(S)))
        print()

        print('3) B перевіряє підпис A:')
        print('k = S^e mod n: {}'.format(check))
        print()
        '''