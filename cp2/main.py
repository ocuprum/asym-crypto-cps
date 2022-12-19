import RSA.RSA as rsa 
from RSA.RSAfuncs import to_hex

while True:
    print('1 - Ввести ServerKey')
    print('2 - Створити нового користувача')
    print('3 - Cтворити новий протокол')
    print('0 - Завершити роботу')

    answer = int(input('\nОберіть потрібний варіант: '))
    print('----------------------------\n')

    if answer == 0: break

    elif answer == 1:
        server_key_n = input('Введіть Server Key - n: ')
        server_key_e = input('Введіть Server Key - e: ')
        server_key_n, server_key_e = int(server_key_n.lower(), 16), int(server_key_e.lower(), 16)
        print()

    elif answer == 2:
        A = rsa.RSA()
        print('Створено нового користувача RSA')

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
                print('Відкритий ключ користувача - e: {}\n'.format(to_hex(A.e)))
                ciphertext = int(input('Введіть ШТ, отриманий від сервера: ').lower(), 16)
                print('Користувач розшифрував повідомлення: {}'.format(to_hex(A.decrypt(ciphertext))))

            elif answer == 2:
                message = int(input('Введіть повідомлення: '), 16)
                print('Шифротекст для сервера: {}'.format(to_hex(A.encrypt(message, (server_key_n, server_key_e)))))

            elif answer == 3:
                message = int(input('Введіть повідомлення: ').lower(), 16)
                sign = int(input('Введіть підпис сервера: ').lower(), 16)
                print('Перевірка підпису сервера: {}'.format(bool(A.verify((message, sign), (server_key_n, server_key_e)))))

            elif answer == 4:
                message = int(input('Введіть повідомлення: ').lower(), 16)
                print('Відкритий ключ користувача - n: {}'.format(to_hex(A.n)))
                print('Відкритий ключ користувача - e: {}\n'.format(to_hex(A.e)))
                sign = A.sign(message)[1]
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