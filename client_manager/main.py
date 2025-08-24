import utils as utils
import art
import os
import pathlib as plib
import tabulate as tab

os.system("cls")
art.tprint("CLIENT  MANAGER")

root_path = plib.Path(__file__).parent
dir_list = utils.client_list_get(root_path=root_path) #получение все скачаных клиентов

if not dir_list:
    print('На вашем комьпьютере не найдено ни одного клиента PharmNet')
else:
    tab_list = utils.tab_client_print(dir_list)

print('\n')
utils.command_list_print()

while True:
    command = input()
    try:
        match command:
            case t if not t.strip():
                continue
            case t if com:=utils.check_exists_command(command): #комманда найдена
                # print(' '*4+f'Комманда найдена {com}')
                com.func(command, root_path)
            case t if t.strip().startswith(('exit', 'close')):
                print('Выход')
                exit()
            case _:
                print("Неизвестная комманда")
    except Exception as error:
        print(error)