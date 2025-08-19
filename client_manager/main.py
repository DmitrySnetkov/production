import f


print('Вводите команды для работы с менеджером клиентов')
is_loop = True



while True:
    command = input()
    try:
        match command:
            case t if t.strip().startswith('add'):
                print('add')
                f.f_add(r'C:\Users\User\Desktop\программирование\production\production')
            case t if t.strip().startswith('update all'):
                print('update all')
            case t if t.strip().startswith('update'):
                print('update')
                f.f_add(r'C:\Users\User\Desktop\программирование\production\production')
            # case t if t.strip().startswith('copy'):
            #     print('copy')
            case t if t.strip().startswith('delete'):
                print('delete')
            case t if t.strip().startswith('run'):
                print('run')
            case t if t.strip().startswith('exit'):
                print('exit')
                exit()
            case _:
                print("Неизвестная комманда")
    except Exception as error:
        print(error)